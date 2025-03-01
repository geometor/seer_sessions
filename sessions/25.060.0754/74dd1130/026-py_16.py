"""
The transformation rule identified in the Dream phase involves a specific pixel-swapping operation within 3x3 subgrids. The swapping occurs only if a 3x3 subgrid is completely filled with the same non-white (non-0) color. If the condition is met, a series of swaps are performed.

This code refines the original by adding a check for uniformity within the 3x3 subgrid before applying the swap.  The condition checks if all elements within the 3x3 sub-grid are identical and not equal to 0 (white).
"""

import numpy as np

def _swap_pixels(grid, row, col):
    # Swap top-left and top-right pixels.
    grid[row, col], grid[row, col + 2] = grid[row, col + 2], grid[row, col]

    # Swap bottom-left and bottom-right pixels.
    grid[row + 2, col], grid[row + 2, col + 2] = grid[row + 2, col + 2], grid[row + 2, col]

    # Swap top-middle and left-middle pixels.
    grid[row, col + 1], grid[row + 1, col] = grid[row + 1, col], grid[row, col + 1]

    # Swap bottom-middle and right-middle pixels.
    grid[row + 2, col + 1], grid[row + 1, col + 2] = grid[row + 1, col + 2], grid[row + 2, col + 1]
    return grid

def _is_uniform_non_white(grid, row, col):
    # Extract the 3x3 subgrid.
    subgrid = grid[row:row+3, col:col+3]
    # Check if all elements are identical and not equal to 0.
    first_element = subgrid.flatten()[0]
    if first_element == 0:
       return False
    return np.all(subgrid == first_element)

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through all possible 3x3 subgrids.
    for row in range(height - 2):
        for col in range(width - 2):
            # Check if the 3x3 subgrid is uniform and not white (color 0)
            if _is_uniform_non_white(output_grid, row, col):
                # Apply the pixel-swapping transformation to the current 3x3 subgrid.
                output_grid = _swap_pixels(output_grid, row, col)

    return output_grid