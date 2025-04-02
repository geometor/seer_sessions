import numpy as np
from typing import List

"""
Transformation Rule:
1. Identify the single orange pixel (7) and its index.
2. Identify the contiguous block of pixels that are neither white (0) nor orange (7) (the 'moving object').
3. Collect all white pixels (0) that appear *before* the orange pixel in the input.
4. Collect all white pixels (0) that appear *after* the orange pixel in the input.
5. Construct the output array by concatenating:
    a. The collected 'before' white pixels.
    b. The identified 'moving object' block.
    c. The single orange pixel (7).
    d. The collected 'after' white pixels.
"""

def find_pixel_index(grid_row: List[int], target_color: int) -> int:
    """Finds the index of the first occurrence of target_color in the row."""
    for i, pixel in enumerate(grid_row):
        if pixel == target_color:
            return i
    return -1 # Should not happen based on task description

def find_moving_object(grid_row: List[int]) -> List[int]:
    """Finds the contiguous block of non-white (0) and non-orange (7) pixels."""
    moving_object = []
    for pixel in grid_row:
        if pixel != 0 and pixel != 7:
            moving_object.append(pixel)
    return moving_object # Assumes only one such block exists and extracts its pixels

def collect_white_pixels(grid_row: List[int], orange_index: int) -> (List[int], List[int]):
    """Collects white pixels before and after the orange pixel's index."""
    leading_whites = []
    trailing_whites = []
    for i, pixel in enumerate(grid_row):
        if pixel == 0:
            if i < orange_index:
                leading_whites.append(pixel)
            else: # i > orange_index (since orange pixel itself isn't white)
                trailing_whites.append(pixel)
    return leading_whites, trailing_whites

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Rearranges a 1D grid by moving a colored block to be left-adjacent
    to the orange pixel (7), grouping white pixels (0) before and after.

    Args:
        input_grid: A list containing a single list (the 1D row of pixels).

    Returns:
        A list containing a single list representing the transformed 1D row.
    """
    # Since the grid is 1D, work with the first row
    input_row = input_grid[0]

    # 1. Find the orange pixel's index
    orange_index = find_pixel_index(input_row, 7)
    if orange_index == -1:
         # Handle error case or unexpected input if necessary
         # For ARC, we usually assume valid inputs per examples
         return input_grid # Or raise an error

    # 2. Find the moving object (the non-white, non-orange block)
    moving_object = find_moving_object(input_row)

    # 3. & 4. Collect white pixels before and after the orange pixel
    leading_whites, trailing_whites = collect_white_pixels(input_row, orange_index)

    # 5. Construct the output row
    output_row = leading_whites + moving_object + [7] + trailing_whites

    # Wrap the output row in a list to match the expected output grid format
    output_grid = [output_row]

    return output_grid
