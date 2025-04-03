import numpy as np
from typing import List

"""
Transformation Rule:
1. Identify the first contiguous block of non-white (non-zero) pixels from the left of the sequence.
2. Identify the contiguous block of white (zero) pixels that immediately follows the non-white block.
3. Swap the positions of these two blocks.
4. Keep all other pixels (leading white pixels and pixels after the swapped blocks) in their original relative positions.
"""

def find_first_non_white_block(grid: List[int]) -> tuple[int, int]:
    """Finds the start and end indices of the first non-white block."""
    start_index = -1
    end_index = -1
    n = len(grid)

    # Find the start of the first non-white block
    for i in range(n):
        if grid[i] != 0:
            start_index = i
            break
            
    # If no non-white pixel found, return (-1, -1)
    if start_index == -1:
        return -1, -1

    # Find the end of the first non-white block
    end_index = start_index
    for i in range(start_index + 1, n):
        if grid[i] != 0:
            end_index = i
        else:
            break # End of the non-white block

    return start_index, end_index

def find_subsequent_white_block(grid: List[int], start_search_index: int) -> tuple[int, int]:
    """Finds the start and end indices of the white block starting at start_search_index."""
    start_index = -1
    end_index = -1
    n = len(grid)

    # Check if the search starts within bounds and if the pixel is white
    if start_search_index >= n or grid[start_search_index] != 0:
        return -1, -1 # No white block starts immediately after

    start_index = start_search_index
    end_index = start_index
    # Find the end of the white block
    for i in range(start_index + 1, n):
        if grid[i] == 0:
            end_index = i
        else:
            break # End of the white block

    return start_index, end_index

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid (sequence).
    Finds the first non-white block and the immediately following white block,
    then swaps their positions.
    """
    n = len(input_grid)

    # 1. Find the first contiguous block of non-white pixels.
    nw_start, nw_end = find_first_non_white_block(input_grid)

    # If no non-white block is found, return the original grid
    if nw_start == -1:
        return input_grid

    # 2. Find the contiguous block of white pixels immediately following.
    w_start_search = nw_end + 1
    w_start, w_end = find_subsequent_white_block(input_grid, w_start_search)

    # If no subsequent white block is found, return the original grid
    if w_start == -1:
        return input_grid

    # 3. Extract the different segments of the grid
    leading_pixels = input_grid[0:nw_start]
    non_white_block = input_grid[nw_start : nw_end + 1]
    white_block = input_grid[w_start : w_end + 1]
    remainder = input_grid[w_end + 1 :]

    # 4. Construct the output grid by rearranging the segments
    output_grid = leading_pixels + white_block + non_white_block + remainder

    return output_grid
