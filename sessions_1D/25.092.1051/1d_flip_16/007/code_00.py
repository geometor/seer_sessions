import copy
from collections import Counter
import numpy as np # Import numpy to handle potential numpy array inputs

"""
Transforms a 1xN input grid by identifying the first contiguous segment of non-zero pixels. 
Within this segment, there must be exactly two distinct non-zero colors: one appearing 
once ('singleton') and the other appearing multiple times contiguously ('block'). 
The transformation swaps the relative positions of the singleton pixel and the block 
of pixels within the segment, leaving the surrounding zero pixels (background) unchanged.
If the input structure does not match this pattern (e.g., no non-zero segment, wrong number 
of colors, block not contiguous), the original grid is returned.
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
        # Use explicit comparison to handle potential numpy numeric types
        if pixel != 0: 
            if not in_segment:
                start_index = i
                in_segment = True
            end_index = i 
        elif in_segment: 
            # We found the end of the first contiguous segment
            break 
    
    if not in_segment: # No non-zero elements found at all
        return -1, -1
        
    return start_index, end_index

def analyze_segment(segment):
    """
    Analyzes a segment of pixels to find the singleton and block colors/lengths. 
    Verifies the expected structure (two distinct non-zero colors, one singleton, one contiguous block).

    Args:
        segment (list): The list of pixel values from the active segment.

    Returns:
        tuple: (singleton_color, block_color, block_length). 
               Returns (-1, -1, 0) if the expected structure is not found.
    """
    if not segment:
        return -1, -1, 0

    # Ensure we only count non-zero pixels within the provided segment
    non_zero_pixels = [p for p in segment if p != 0]
    if not non_zero_pixels:
         return -1, -1, 0
         
    counts = Counter(non_zero_pixels)

    singleton_color = -1
    block_color = -1
    block_length = 0

    # Expect exactly two distinct non-zero colors
    if len(counts) != 2: 
         return -1, -1, 0

    # Identify singleton and block based on counts
    for color, count in counts.items():
        # Convert color to int just in case it's a numpy numeric type
        color_int = int(color) 
        if count == 1:
            singleton_color = color_int
        elif count > 1:
            block_color = color_int
            block_length = count

    # Final check if both were identified correctly
    if singleton_color == -1 or block_color == -1:
        return -1, -1, 0

    # Verify the block is contiguous
    try:
        # Find first occurrence index
        first_block_idx = -1
        for idx, p in enumerate(segment):
            if p == block_color:
                first_block_idx = idx
                break
        
        if first_block_idx == -1: # Should not happen if counter found it
             return -1, -1, 0

        # Check if the slice starting from first_block_idx of length block_length are all block_color
        is_contiguous = True
        if first_block_idx + block_length > len(segment): # Block would extend beyond segment
            is_contiguous = False
        else:
            for i in range(block_length):
                if segment[first_block_idx + i] != block_color:
                    is_contiguous = False
                    break
        
        # Also check that no other block_color pixels exist outside this contiguous range
        other_block_pixels = False
        for i in range(len(segment)):
            if i >= first_block_idx and i < first_block_idx + block_length:
                continue # Skip the contiguous block itself
            if segment[i] == block_color:
                other_block_pixels = True
                break

        if not is_contiguous or other_block_pixels:
             return -1, -1, 0
             
    except Exception: # Catch potential errors during check
        return -1, -1, 0
        
    return singleton_color, block_color, block_length

def transform(input_grid):
    """
    Transforms the input grid by swapping a singleton and block within the active segment.
    Handles both list of lists and numpy array inputs.
    """
    # --- 1. Input Handling and Initialization ---
    # Check for basic validity and get the row
    if input_grid is None: return [] # Handle None input
    
    input_row_orig = None
    if isinstance(input_grid, np.ndarray):
        if input_grid.ndim == 2 and input_grid.shape[0] == 1:
            input_row_orig = input_grid[0]
        elif input_grid.ndim == 1: # Allow 1D numpy array as input row directly
            input_row_orig = input_grid
        else:
             return [] # Invalid numpy array shape
    elif isinstance(input_grid, list):
        if len(input_grid) == 1 and isinstance(input_grid[0], list):
             input_row_orig = input_grid[0]
        elif all(isinstance(item, (int, np.integer)) for item in input_grid): # Check if it's a flat list (like a direct row)
             input_row_orig = input_grid # Allow flat list input
        else:
            return [] # Invalid list structure
    else:
        return [] # Invalid input type

    # Ensure working with standard Python list of ints
    try:
        input_row = [int(p) for p in input_row_orig]
    except (ValueError, TypeError):
        return copy.deepcopy(input_grid) # Return original if conversion fails

    # Create a mutable copy for the output
    output_row = list(input_row) 

    # --- 2. Identify Active Segment ---
    start_index, end_index = find_active_segment_indices(input_row)

    # If no non-zero segment found, return the original grid formatted correctly
    if start_index == -1:
        # Ensure output is list of lists
        if isinstance(input_grid, np.ndarray) and input_grid.ndim == 1:
            return [input_row] # Wrap 1D array input row
        elif isinstance(input_grid, list) and not isinstance(input_grid[0], list):
             return [input_row] # Wrap flat list input row
        else:
             return copy.deepcopy(input_grid) 


    # --- 3. Extract Active Segment ---
    segment = input_row[start_index : end_index + 1]

    # --- 4. Analyze Segment: Find Singleton and Block ---
    singleton_color, block_color, block_length = analyze_segment(segment)

    # If analysis failed (unexpected format), return original grid formatted correctly
    if singleton_color == -1 or block_color == -1:
         # print(f"Warning: Segment analysis failed for segment {segment}. Returning original grid.")
        if isinstance(input_grid, np.ndarray) and input_grid.ndim == 1:
            return [input_row] 
        elif isinstance(input_grid, list) and not isinstance(input_grid[0], list):
             return [input_row]
        else:
            return copy.deepcopy(input_grid)

    # --- 5. Determine Original Order ---
    starts_with_singleton = (segment[0] == singleton_color)
    
    # Verify segment starts with either the singleton or the block
    if not starts_with_singleton and segment[0] != block_color:
        # This implies an unexpected structure not caught by analyze_segment
        # print(f"Warning: Segment {segment} doesn't start with identified singleton ({singleton_color}) or block ({block_color}). Returning original.")
        if isinstance(input_grid, np.ndarray) and input_grid.ndim == 1:
            return [input_row] 
        elif isinstance(input_grid, list) and not isinstance(input_grid[0], list):
             return [input_row]
        else:
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
        # print(f"Error: New segment length ({len(new_segment)}) does not match original ({len(segment)}).")
        # Return original on internal error
        if isinstance(input_grid, np.ndarray) and input_grid.ndim == 1:
            return [input_row]
        elif isinstance(input_grid, list) and not isinstance(input_grid[0], list):
             return [input_row]
        else:
             return copy.deepcopy(input_grid)

    # --- 7. Reconstruct Output List ---
    # Replace the original segment slice in the output row copy with the new segment
    output_row[start_index : end_index + 1] = new_segment
    
    # --- 8. Format Output ---
    # Wrap the final output row back into a 1xN grid (list of lists)
    output_grid = [output_row]

    return output_grid