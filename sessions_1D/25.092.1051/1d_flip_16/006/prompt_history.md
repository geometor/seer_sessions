
## train_1

**input:**
```
0 0 5 8 8 8 8 8 8 8 0 0 0 0 0 0
```


**output:**
```
0 0 8 8 8 8 8 8 8 5 0 0 0 0 0 0
```


## train_2

**input:**
```
0 1 8 8 8 8 8 8 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 8 8 8 8 8 1 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 4 5 5 5 5 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 5 5 5 4 0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The input and output are 1D arrays (or 1xN grids) of integers representing colors. The transformation appears to operate on a specific segment of the array containing non-zero values, leaving the surrounding zero values (white pixels) unchanged. Within the non-zero segment, there are always two distinct non-zero colors present: one color appears as a single pixel (the "singleton"), and the other appears as a contiguous block of multiple pixels (the "block"). The core transformation is the swapping of the relative positions of the singleton pixel and the block of pixels.

**Facts:**


```yaml
task_type: array_manipulation
grid_dimensionality: 1D # Effectively 1D arrays presented
background_color: 0 # white
objects:
  - name: singleton
    description: A single pixel of a non-zero color within the active segment.
    properties:
      - color: variable (5 in train_1, 1 in train_2, 4 in train_3)
      - count: 1
  - name: block
    description: A contiguous sequence of pixels of the same non-zero color within the active segment.
    properties:
      - color: variable (8 in train_1, 8 in train_2, 5 in train_3)
      - count: >1
      - contiguous: true
relationships:
  - type: adjacency
    objects: [singleton, block]
    description: The singleton and the block are always adjacent to each other in the input.
  - type: boundary
    objects: [singleton, block, background_color]
    description: The combined singleton and block form a contiguous segment surrounded by the background color (0).
actions:
  - name: identify_active_segment
    description: Find the contiguous subsequence of non-zero pixels.
  - name: identify_singleton_and_block
    description: Within the active segment, differentiate the pixel appearing once (singleton) from the pixel color appearing multiple times contiguously (block).
  - name: swap_position
    objects: [singleton, block]
    description: Reverse the order of the singleton and the block within the active segment.
  - name: reconstruct_output
    description: Place the modified active segment back into its original position relative to the surrounding background pixels.
```


**Natural Language Program:**

1.  Identify the start and end indices of the contiguous segment containing non-zero pixels in the input array.
2.  Extract this non-zero segment.
3.  Within the extracted segment, count the occurrences of each unique non-zero color.
4.  Identify the color that appears exactly once; this is the 'singleton' color.
5.  Identify the color that appears multiple times; this constitutes the 'block' color and its associated pixels.
6.  Create a new segment by placing the block pixels first, followed by the singleton pixel, if the singleton was originally first. Otherwise (if the block was originally first), place the singleton pixel first, followed by the block pixels. Essentially, swap their order.
7.  Construct the output array by replacing the original non-zero segment (between the identified start and end indices) with the newly created swapped segment. Keep all zero pixels outside this segment in their original positions.
```python
import numpy as np
from collections import Counter
import copy

"""
Identifies a contiguous segment of non-zero pixels within a 1D input array. 
Within this segment, it finds a single pixel ('singleton') of one color and a 
contiguous block of pixels ('block') of another color. The transformation 
swaps the relative positions of the singleton and the block within the segment, 
leaving the surrounding zero pixels unchanged.
"""

def find_active_segment_indices(row):
  """Finds the start and end indices of the first contiguous non-zero segment."""
  start_index = -1
  end_index = -1
  for i, pixel in enumerate(row):
    if pixel != 0:
      if start_index == -1:
        start_index = i
      end_index = i # Keep updating end_index for the last non-zero element
  # Adjust end_index to be inclusive
  return start_index, end_index

def transform(input_grid):
    """
    Transforms the input grid by swapping a singleton pixel and a block of pixels
    within the non-zero segment of the grid.

    Args:
        input_grid (list of lists): A 1xN grid represented as a list containing one list.

    Returns:
        list of lists: The transformed 1xN grid.
    """
    # Ensure input is treated as a 1D array (list)
    # ARC grids are list of lists, even if 1D
    if not input_grid or not input_grid[0]:
        return [] # Handle empty input
        
    input_row = input_grid[0]
    output_row = list(input_row) # Create a mutable copy

    # 1. Identify the start and end indices of the contiguous non-zero segment.
    start_index, end_index = find_active_segment_indices(input_row)

    # If no non-zero segment found, return the original grid
    if start_index == -1:
        return copy.deepcopy(input_grid) # Return a copy to avoid modifying original

    # 2. Extract this non-zero segment.
    # Note: end_index from find_active_segment_indices is inclusive
    segment = input_row[start_index : end_index + 1]

    # 3. Within the extracted segment, count the occurrences of each unique non-zero color.
    non_zero_pixels = [p for p in segment if p != 0]
    if not non_zero_pixels: # Should not happen if start_index != -1, but good check
         return copy.deepcopy(input_grid)
         
    counts = Counter(non_zero_pixels)

    # 4. Identify the 'singleton' color.
    singleton_color = -1
    block_color = -1
    block_length = 0

    for color, count in counts.items():
        if count == 1:
            singleton_color = color
        elif count > 1:
            block_color = color
            block_length = count
            
    # Check if both singleton and block were found
    if singleton_color == -1 or block_color == -1:
        # This case might indicate an unexpected input format, return original
        # Or handle based on specific task rules if this is expected.
        # For this specific task, it seems a singleton and block are always present.
        print(f"Warning: Could not identify both singleton ({singleton_color}) and block ({block_color}) in segment {segment}")
        return copy.deepcopy(input_grid)


    # 5. Identify the 'block' color and its associated pixels (already done above).

    # 6. Create a new segment by swapping the order.
    # Determine the original order by checking the first element of the segment
    new_segment = []
    if segment[0] == singleton_color:
        # Original: Singleton then Block
        # New: Block then Singleton
        new_segment.extend([block_color] * block_length)
        new_segment.append(singleton_color)
    elif segment[0] == block_color:
         # Original: Block then Singleton
         # New: Singleton then Block
        new_segment.append(singleton_color)
        new_segment.extend([block_color] * block_length)
    else:
        # Should not happen based on problem description (singleton/block are adjacent)
        # If it could happen, need logic to handle segment starting with background (0)
        # or other structure. Given the examples, assuming segment starts with singleton or block.
        print(f"Warning: Segment {segment} doesn't start with identified singleton or block.")
        return copy.deepcopy(input_grid)


    # 7. Construct the output array by replacing the original segment.
    output_row[start_index : end_index + 1] = new_segment
    
    # Wrap the row back into a list of lists
    output_grid = [output_row]

    return output_grid
```
```python
import copy
from collections import Counter

"""
Identifies a contiguous segment of non-zero pixels within a 1D input row (represented as a 1xN grid). 
Within this segment, it finds a single pixel ('singleton') of one color and a contiguous block 
of pixels ('block') of another color. The transformation swaps the relative positions of the 
singleton and the block within the segment, leaving the surrounding zero pixels unchanged.
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
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start_index == -1:
                start_index = i
            end_index = i  # Keep updating end_index for the last non-zero element
    return start_index, end_index

def analyze_segment(segment):
    """
    Analyzes a segment of non-zero pixels to find the singleton and block colors/lengths.

    Args:
        segment (list): The list of non-zero pixel values from the active segment.

    Returns:
        tuple: (singleton_color, block_color, block_length). 
               Returns (-1, -1, 0) if the expected structure (one singleton, one block color) is not found.
    """
    if not segment:
        return -1, -1, 0

    # Filter out any potential zeros if the definition of segment might include them
    # Although based on find_active_segment_indices logic, it shouldn't
    non_zero_pixels = [p for p in segment if p != 0]
    if not non_zero_pixels:
         return -1, -1, 0
         
    counts = Counter(non_zero_pixels)

    singleton_color = -1
    block_color = -1
    block_length = 0

    if len(counts) != 2: # Expect exactly two distinct non-zero colors
         print(f"Warning: Expected 2 distinct non-zero colors in segment {segment}, found {len(counts)}")
         return -1, -1, 0

    for color, count in counts.items():
        if count == 1:
            singleton_color = color
        elif count > 1:
            block_color = color
            block_length = count
        else: # Should not happen if len(counts) == 2 and one is count=1
             print(f"Warning: Unexpected count {count} for color {color} in segment {segment}")
             return -1, -1, 0

    # Final check if both were identified correctly
    if singleton_color == -1 or block_color == -1:
        print(f"Warning: Could not definitively identify singleton/block in segment {segment}")
        return -1, -1, 0

    return singleton_color, block_color, block_length

def transform(input_grid):
    """
    Transforms the input grid according to the swap rule.

    Args:
        input_grid (list of lists): A 1xN grid represented as a list containing one list.

    Returns:
        list of lists: The transformed 1xN grid.
    """
    # 1. Handle empty input and extract the row
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        # Return empty list or appropriate error handling for invalid format
        return [] 
        
    input_row = input_grid[0]
    # Create a mutable copy for the output
    output_row = list(input_row) 

    # 2. Identify the start and end indices of the active segment.
    start_index, end_index = find_active_segment_indices(input_row)

    # If no non-zero segment found, return the original grid (as a deep copy)
    if start_index == -1:
        return copy.deepcopy(input_grid) 

    # 3. Extract the active segment. Indices are inclusive.
    segment = input_row[start_index : end_index + 1]

    # 4. Analyze the active segment to find singleton and block details.
    singleton_color, block_color, block_length = analyze_segment(segment)

    # If analysis failed (unexpected format), return original grid
    if singleton_color == -1 or block_color == -1:
         print(f"Warning: Segment analysis failed for segment {segment}. Returning original grid.")
         return copy.deepcopy(input_grid)

    # 5. Determine the original order.
    starts_with_singleton = (segment[0] == singleton_color)
    # Add a check to ensure the segment structure is as expected (starts with one or the other)
    if not starts_with_singleton and segment[0] != block_color:
        print(f"Warning: Segment {segment} doesn't start with identified singleton ({singleton_color}) or block ({block_color}). Returning original.")
        return copy.deepcopy(input_grid)
        
    # 6. Construct the new segment by swapping the order.
    new_segment = []
    if starts_with_singleton:
        # Original: Singleton then Block -> New: Block then Singleton
        new_segment.extend([block_color] * block_length)
        new_segment.append(singleton_color)
    else:
        # Original: Block then Singleton -> New: Singleton then Block
        new_segment.append(singleton_color)
        new_segment.extend([block_color] * block_length)
        
    # Verify the length matches the original segment length
    if len(new_segment) != len(segment):
        print(f"Error: New segment length ({len(new_segment)}) does not match original ({len(segment)}). Segment: {segment}, New: {new_segment}")
        return copy.deepcopy(input_grid) # Return original on error

    # 7. Create the output row by replacing the original segment with the new one.
    output_row[start_index : end_index + 1] = new_segment
    
    # 8. Format the output row as a 1xN grid (list of lists).
    output_grid = [output_row]

    return output_grid
```
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
