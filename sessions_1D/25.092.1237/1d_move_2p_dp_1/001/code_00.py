import numpy as np
from typing import List, Tuple

"""
Transformation Rule:
Identify the single red pixel (2). Identify the contiguous block of non-white, non-red pixels located to the left of the red pixel, separated by exactly two white pixels (0). Swap the positions of this colored block and the two white separator pixels. All other pixels remain in their relative positions.
"""

def find_pixel_index(grid: List[int], color: int) -> int:
    """Finds the index of the first pixel with the specified color."""
    try:
        return grid.index(color)
    except ValueError:
        return -1 # Indicate not found

def find_colored_block_indices(grid: List[int], search_end_index: int) -> Tuple[int, int]:
    """
    Finds the start and end indices of a contiguous block of non-white pixels
    ending immediately before search_end_index.
    Assumes the block exists and is preceded by a white pixel or the start of the grid.
    """
    if search_end_index <= 0:
        return -1, -1 # Cannot have a block ending before index 0

    block_end_index = search_end_index - 1
    block_color = grid[block_end_index]

    # Should not be white or red based on problem description
    if block_color == 0 or block_color == 2:
         return -1, -1 # Unexpected color

    block_start_index = block_end_index
    while block_start_index > 0 and grid[block_start_index - 1] == block_color:
        block_start_index -= 1

    return block_start_index, block_end_index

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid (represented as a 1D list).

    1. Finds the red pixel (2).
    2. Identifies the two white pixels (0) immediately to its left.
    3. Identifies the contiguous colored block immediately to the left of the white pixels.
    4. Reconstructs the grid by swapping the colored block and the two white pixels.
    """

    # Find the index of the red pixel (target marker)
    red_index = find_pixel_index(input_grid, 2)
    if red_index == -1:
        # Handle cases where the red pixel isn't found (though not expected based on examples)
        print("Warning: Red pixel not found.")
        return input_grid # Or raise an error

    # Verify the two white separator pixels exist to the left
    if red_index < 2 or input_grid[red_index - 1] != 0 or input_grid[red_index - 2] != 0:
        # Handle cases where the expected white separators aren't present
        print("Warning: Expected white separator pixels not found.")
        return input_grid # Or raise an error

    white_sep_start_index = red_index - 2
    white_separator_segment = input_grid[white_sep_start_index:red_index] # Should be [0, 0]

    # Find the indices of the colored block
    block_start_index, block_end_index = find_colored_block_indices(input_grid, white_sep_start_index)

    if block_start_index == -1:
         # Handle cases where the colored block isn't found correctly
        print("Warning: Colored block not found or invalid.")
        return input_grid # Or raise an error

    # Extract the segments
    leading_segment = input_grid[:block_start_index]
    colored_block_segment = input_grid[block_start_index : block_end_index + 1]
    red_pixel_segment = [input_grid[red_index]] # Just [2]
    trailing_segment = input_grid[red_index + 1 :]

    # Construct the output grid by rearranging the segments
    output_grid = (
        leading_segment +
        white_separator_segment +
        colored_block_segment +
        red_pixel_segment +
        trailing_segment
    )

    return output_grid