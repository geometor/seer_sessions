"""
Transformation Rule:
1.  Take the input grid, which consists of a single row (1xN). Extract this row as a 1D sequence of pixels.
2.  Find the index of the first maroon (9) pixel in the sequence. This marks the boundary. If no maroon pixel is found, return the original input grid.
3.  Divide the sequence into two parts: the "transform region" (pixels before the maroon pixel) and the "suffix" (the maroon pixel and all subsequent pixels). The suffix remains unchanged.
4.  Analyze the "transform region":
    a.  Find the start index of the first non-white pixel. All pixels before this index form the "prefix". If the region starts with a non-white pixel or is empty, the prefix is empty.
    b.  Starting from that first non-white pixel, identify the "colored block", which is the contiguous sequence of identical non-white pixels. Note its content. If no non-white pixel is found in the transform region, skip the rearrangement and proceed to step 6.
    c.  Identify the "white block", which is the contiguous sequence of white (0) pixels that starts *immediately* after the "colored block" ends. If no white pixel immediately follows, or if the colored block extends to the end of the transform region, the white block is empty. Note its content.
5.  Construct the new "transform region" by concatenating the identified parts in the following order: first the "prefix" (if any), then the "white block" (if any), then the "colored block".
6.  Create the final output sequence by concatenating the newly constructed "transform region" with the unchanged "suffix".
7.  Format the final sequence back into a single-row grid (a list containing one list) and return it.
"""

import numpy as np
from typing import List, Tuple, Optional

# === Helper Functions ===

def find_first_occurrence(arr: np.ndarray, value: int) -> int:
    """Finds the index of the first occurrence of a value in a 1D numpy array."""
    indices = np.where(arr == value)[0]
    if len(indices) > 0:
        return indices[0]
    return -1 # Not found

def find_first_contiguous_non_white_block(arr: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the start index, end index (exclusive), and color of the first
    contiguous block of non-white (non-zero) pixels in a 1D array.
    Returns None if no such block is found.
    """
    block_start = -1
    block_color = -1
    # Find the start of the block and its color
    for i in range(len(arr)):
        # We assume any non-zero value can start the block
        if arr[i] != 0:
            block_start = i
            block_color = arr[i]
            break

    if block_start == -1:
        return None # Block not found

    # Find the end of the block (where color changes or array ends)
    block_end = block_start
    for i in range(block_start, len(arr)):
        if arr[i] == block_color:
            block_end = i + 1
        else:
            break # End of contiguous block of the same color

    return block_start, block_end, block_color

def find_contiguous_white_block_after(arr: np.ndarray, search_start_index: int) -> Optional[Tuple[int, int]]:
    """
    Finds the start and end (exclusive) indices of a contiguous block of
    white (zero) pixels, starting the search *exactly* at search_start_index.
    Returns None if the pixel at search_start_index is not white
    or if search_start_index is out of bounds.
    """
    if search_start_index >= len(arr) or arr[search_start_index] != 0:
        return None # No white block starts here

    block_start = search_start_index
    block_end = block_start
    # Find the end of the block
    for i in range(block_start, len(arr)):
        if arr[i] == 0:
            block_end = i + 1
        else:
            break # End of contiguous white block

    return block_start, block_end


# === Main Transformation Function ===

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to a 1xN input grid.
    """
    # 1. Extract the single row
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
         # Handle invalid or empty input grid format
        return input_grid # Return as is for invalid format
    input_row_list = input_grid[0]
    input_arr = np.array(input_row_list, dtype=int)

    # Handle case of completely empty row inside the grid
    if input_arr.size == 0:
        return input_grid

    # 2. Locate the marker (maroon pixel, value 9)
    marker_index = find_first_occurrence(input_arr, 9)

    # If no marker is found, return the input grid as is
    if marker_index == -1:
        return input_grid

    # 3. Partition the input array
    transform_region = input_arr[:marker_index]
    suffix = input_arr[marker_index:]

    # 4. Analyze the transform region
    # 4b. Find the colored block
    colored_block_info = find_first_contiguous_non_white_block(transform_region)

    # If no colored block found, the transform region remains unchanged
    if colored_block_info is None:
        # Reconstruct the original row and return in grid format
        # No change needed, just reassemble transform_region and suffix
        output_row = np.concatenate((transform_region, suffix)).tolist()
        return [output_row]

    colored_block_start, colored_block_end, _ = colored_block_info
    colored_block = transform_region[colored_block_start:colored_block_end]

    # 4a. Identify the prefix (elements before the colored block)
    prefix = transform_region[:colored_block_start]

    # 4c. Identify the contiguous white block immediately following the colored block
    white_block_info = find_contiguous_white_block_after(transform_region, colored_block_end)

    # Extract the white block content
    white_block = np.array([], dtype=int) # Default to empty
    if white_block_info is not None:
        white_block_start, white_block_end = white_block_info
        # Double check it started exactly after the colored block
        # (find_contiguous_white_block_after already ensures this by design)
        white_block = transform_region[white_block_start:white_block_end]


    # 5. Construct the new arrangement for the transform region
    # Use a list to gather parts, handling empty arrays correctly
    parts_to_join = []
    if prefix.size > 0:
        parts_to_join.append(prefix)
    if white_block.size > 0:
        parts_to_join.append(white_block)
    if colored_block.size > 0: # Should always be > 0 if colored_block_info was not None
         parts_to_join.append(colored_block)

    # Concatenate the parts if any exist
    if parts_to_join:
      new_transform_region = np.concatenate(parts_to_join)
    else:
      # This case implies transform_region was empty or all white pixels,
      # and colored_block_info would have been None, handled earlier.
      # If somehow we get here (e.g., empty colored block found?),
      # default to original transform region.
      new_transform_region = transform_region


    # 6. Combine the new transform region with the suffix
    output_arr = np.concatenate((new_transform_region, suffix))

    # 7. Convert back to list and wrap in list for the expected 1xN grid output format
    output_grid = [output_arr.tolist()]

    return output_grid