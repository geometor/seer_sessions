```python
import copy
from collections import Counter

"""
Transforms a 1xN input grid by identifying a contiguous segment of non-zero pixels. 
Within this segment, there must be exactly two distinct non-zero colors: one 
appearing once ('singleton') and the other appearing multiple times contiguously 
('block'). The transformation swaps the relative positions of the singleton pixel 
and the block of pixels within the segment, leaving the surrounding zero pixels 
(background) unchanged.
"""

def find_active_segment_indices(row):
    """
    Finds the start and end indices (inclusive) of the first contiguous non-zero segment in a list.

    Args:
        row (list): A list of pixel values.

    Returns:
        tuple: A tuple (start_index, end_index). Returns (-1, -1) if no non-zero segment is found.
    """
    start_index = -1
    end_index = -1
    in_segment = False
    for i, pixel in enumerate(row):
        if pixel != 0:
            if not in_segment:
                start_index = i
                in_segment = True
            end_index = i 
        elif in_segment: 
            # We found the end of the first contiguous segment
            break 
            # Note: If multiple segments are possible, this only finds the first.
            # Based on examples, only one segment seems relevant.
            
    # If loop finished while in_segment, end_index is already correct.
    # If loop finished before finding non-zero, start_index is -1.
    
    # Handle edge case where the segment goes to the end of the list: end_index is already correctly set.

    if not in_segment: # No non-zero elements found at all
        return -1, -1
        
    return start_index, end_index

def analyze_segment(segment):
    """
    Analyzes a segment of non-zero pixels to find the singleton and block colors/lengths.

    Args:
        segment (list): The list of pixel values from the active segment. 
                        Should ideally contain only non-zero values from that segment.

    Returns:
        tuple: (singleton_color, block_color, block_length). 
               Returns (-1, -1, 0) if the expected structure (one singleton, one block color) is not found.
    """
    if not segment:
        return -1, -1, 0

    # Ensure we only count non-zero pixels within the provided segment
    non_zero_pixels = [p for p in segment if p != 0]
    if not non_zero_pixels:
         # This case means the segment passed in was all zeros, shouldn't happen
         # if find_active_segment_indices worked correctly.
         return -1, -1, 0
         
    counts = Counter(non_zero_pixels)

    singleton_color = -1
    block_color = -1
    block_length = 0

    # Expect exactly two distinct non-zero colors based on problem description
    if len(counts) != 2: 
         # print(f"Warning: Expected 2 distinct non-zero colors in segment {segment}, found {len(counts)}")
         return -1, -1, 0

    # Identify singleton and block based on counts
    for color, count in counts.items():
        if count == 1:
            singleton_color = color
        elif count > 1:
            block_color = color
            block_length = count
        # else: Should not happen if len(counts) == 2 and one has count 1

    # Final check if both were identified correctly
    if singleton_color == -1 or block_color == -1:
        # print(f"Warning: Could not definitively identify singleton/block in segment {segment}")
        return -1, -1, 0

    # Verify contiguous block (optional but good practice)
    # Find first and last occurrence of block_color
    try:
        first_block_idx = segment.index(block_color)
        last_block_idx = len(segment) - 1 - segment[::-1].index(block_color)
        # Check if all elements between first and last are the block color
        is_contiguous = all(p == block_color for p in segment[first_block_idx : last_block_idx + 1])
        # Check if the count matches the span
        if not is_contiguous or (last_block_idx - first_block_idx + 1) != block_length:
             # print(f"Warning: Block color {block_color} is not contiguous or length mismatch in segment {segment}")
             return -1, -1, 0
    except ValueError: # Should not happen if block_color was found by Counter
        # print(f"Error: Block color {block_color} not found in segment {segment} during contiguity check.")
        return -1, -1, 0
        

    return singleton_color, block_color, block_length

def transform(input_grid):
    """
    Transforms the input grid by swapping a singleton and block within the active segment.
    """
    # --- 1. Input Handling and Initialization ---
    # Expecting a 1xN grid (list containing one list)
    if not input_grid or not isinstance(input_grid, list) or len(input_grid) != 1 or \
       not input_grid[0] or not isinstance(input_grid[0], list):
        # Return empty list for invalid format based on ARC structure
        return [] 
        
    input_row = input_grid[0]
    # Create a mutable copy for the output
    output_row = list(input_row) 

    # --- 2. Identify Active Segment ---
    start_index, end_index = find_active_segment_indices(input_row)

    # If no non-zero segment found, return the original grid (as a deep copy)
    if start_index == -1:
        return copy.deepcopy(input_grid) 

    # --- 3. Extract Active Segment ---
    # Indices from find_active_segment_indices are inclusive
    segment = input_row[start_index : end_index + 1]

    # --- 4. Analyze Segment: Find Singleton and Block ---
    singleton_color, block_color, block_length = analyze_segment(segment)

    # If analysis failed (unexpected format), return original grid
    if singleton_color == -1 or block_color == -1:
         # print(f"Warning: Segment analysis failed for segment {segment}. Returning original grid.")
         return copy.deepcopy(input_grid)

    # --- 5. Determine Original Order ---
    # Check if the segment starts with the singleton or the block
    starts_with_singleton = (segment[0] == singleton_color)
    
    # Verify segment starts with either the singleton or the block
    if not starts_with_singleton and segment[0] != block_color:
        # This implies the segment has an unexpected structure, e.g., internal zeros
        # or more than two components, which analyze_segment should ideally catch.
        # print(f"Warning: Segment {segment} doesn't start with identified singleton ({singleton_color}) or block ({block_color}). Returning original.")
        return copy.deepcopy(input_grid)
        
    # --- 6. Construct New Swapped Segment ---
    new_segment = []
    if starts_with_singleton:
        # Original: Singleton then Block -> New: Block then Singleton
        new_segment.extend([block_color] * block_length)
        new_segment.append(singleton_color)
    else: # Starts with block
        # Original: Block then Singleton -> New: Singleton then Block
        new_segment.append(singleton_color)
        new_segment.extend([block_color] * block_length)
        
    # Sanity check: ensure the new segment has the same length as the old one
    if len(new_segment) != len(segment):
        # print(f"Error: New segment length ({len(new_segment)}) does not match original ({len(segment)}). Segment: {segment}, New: {new_segment}")
        # This indicates a potential logic error in analysis or reconstruction.
        return copy.deepcopy(input_grid) # Return original on error

    # --- 7. Reconstruct Output List ---
    # Replace the original segment slice in the output row copy with the new segment
    output_row[start_index : end_index + 1] = new_segment
    
    # --- 8. Format Output ---
    # Wrap the final output row back into a 1xN grid (list of lists)
    output_grid = [output_row]

    return output_grid
```