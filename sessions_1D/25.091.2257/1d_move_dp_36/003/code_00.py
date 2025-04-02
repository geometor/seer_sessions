import numpy as np
from typing import List, Tuple

"""
Transformation rule:
1.  Take the input, which is a grid with a single row (1xN). Extract this row for processing.
2.  Locate the index of the first maroon (9) pixel within the row. This marks the boundary.
3.  Separate the row into two parts: the "transform region" (all pixels *before* the maroon pixel) and the "suffix" (the maroon pixel and all pixels after it). The "suffix" will remain unchanged.
4.  Analyze the "transform region":
    a.  Identify the "prefix": the sequence of pixels from the start of the transform region up to, but not including, the first non-white pixel. (Based on examples, the prefix consists only of white pixels).
    b.  Identify the "colored block": the first contiguous sequence of identical non-white pixels. Note its color and length.
    c.  Identify the "white block": the contiguous sequence of white (0) pixels that *immediately* follows the "colored block". Note its length. If no white pixels immediately follow, this block has length 0.
5.  Construct the new "transform region" for the output row by concatenating the identified parts in this specific order: first the "prefix", then the "white block", then the "colored block".
6.  Create the final output row by concatenating the newly constructed "transform region" with the original unchanged "suffix".
7.  Format the final output row back into a 1xN grid (a list containing one list).
"""

def find_first_occurrence(arr: np.ndarray, value: int) -> int:
    """Finds the index of the first occurrence of a value in a 1D numpy array."""
    indices = np.where(arr == value)[0]
    if len(indices) > 0:
        return indices[0]
    return -1 # Not found

def find_first_contiguous_non_white_block(arr: np.ndarray) -> Tuple[int, int, int]:
    """
    Finds the start index, end index (exclusive), and color of the first
    contiguous block of non-white (non-zero) pixels in a 1D array.
    Returns (-1, -1, -1) if no such block is found.
    """
    block_start = -1
    block_color = -1
    # Find the start of the block and its color
    for i in range(len(arr)):
        if arr[i] != 0:
            block_start = i
            block_color = arr[i]
            break

    if block_start == -1:
        return -1, -1, -1 # Block not found

    # Find the end of the block
    block_end = block_start
    for i in range(block_start, len(arr)):
        if arr[i] == block_color:
            block_end = i + 1
        else:
            break # End of contiguous block of the same color

    return block_start, block_end, block_color

def find_contiguous_white_block(arr: np.ndarray, start_index: int) -> Tuple[int, int]:
    """
    Finds the start and end (exclusive) indices of a contiguous block of
    white (zero) pixels, starting the search *exactly* at start_index.
    Returns (start_index, start_index) if the pixel at start_index is not white
    or if start_index is out of bounds.
    """
    if start_index >= len(arr) or arr[start_index] != 0:
        return start_index, start_index # No white block starts here

    block_start = start_index
    block_end = block_start
    # Find the end of the block
    for i in range(block_start, len(arr)):
        if arr[i] == 0:
            block_end = i + 1
        else:
            break # End of contiguous white block

    return block_start, block_end


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to a 1xN input grid.
    """
    # 1. Extract the single row
    if not input_grid or not input_grid[0]:
        return input_grid # Handle empty input case
    input_row_list = input_grid[0]
    input_arr = np.array(input_row_list, dtype=int)

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
    colored_block_start, colored_block_end, _ = find_first_contiguous_non_white_block(transform_region)

    # If no colored block found, the transform region remains unchanged
    if colored_block_start == -1:
        # Reconstruct the original row and return in grid format
        output_row = np.concatenate((transform_region, suffix)).tolist()
        return [output_row]

    # Extract the colored block content
    colored_block = transform_region[colored_block_start:colored_block_end]

    # 4a. Identify the prefix (elements before the colored block)
    prefix = transform_region[:colored_block_start]

    # 4c. Identify the contiguous white block immediately following the colored block
    white_block_start, white_block_end = find_contiguous_white_block(transform_region, colored_block_end)

    # Extract the white block content
    # white_block_start will equal colored_block_end if a white block starts there
    if white_block_start == colored_block_end:
        white_block = transform_region[white_block_start:white_block_end]
    else:
        # No adjacent white block found
        white_block = np.array([], dtype=int)

    # 5. Construct the new arrangement for the transform region
    new_transform_region_list = []
    if prefix.size > 0:
        new_transform_region_list.append(prefix)
    if white_block.size > 0:
        new_transform_region_list.append(white_block)
    if colored_block.size > 0:
         new_transform_region_list.append(colored_block)

    # Concatenate the parts if they exist
    if new_transform_region_list:
      new_transform_region = np.concatenate(new_transform_region_list)
    else:
      # This case might happen if the transform region was empty or only white
      new_transform_region = transform_region # Keep original if no blocks rearranged


    # 6. Combine the new transform region with the suffix
    output_arr = np.concatenate((new_transform_region, suffix))

    # 7. Convert back to list and wrap in list for the expected 1xN grid output format
    output_grid = [output_arr.tolist()]

    return output_grid