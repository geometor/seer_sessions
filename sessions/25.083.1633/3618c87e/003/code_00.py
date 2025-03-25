"""
1.  Identify the bottom row of the grid.
2.  Locate all blue (1) pixels: For each blue pixel, move it to the bottom row of the grid, in the same column.
3.  Locate all gray (5) pixels:
    *   If the gray pixel *is not* already on the bottom row, move it to the bottom row, maintaining the same column.
    *   If in a location where blue will land. blue overwrites gray.
4.  Clear all other rows except bottom row. Set all pixels in rows above the bottom row to black (0).
"""

import numpy as np

def get_bottom_row_index(grid):
    """Finds the index of the bottom row."""
    return grid.shape[0] - 1

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a given color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape
    bottom_row_index = get_bottom_row_index(output_grid)

    # Initialize the bottom row with gray (5)
    output_grid[bottom_row_index, :] = 5

    # Move blue (1) pixels to the bottom row, overwriting gray
    blue_pixels = find_pixels_by_color(input_grid, 1)
    for r, c in blue_pixels:
        output_grid[bottom_row_index, c] = 1
        
    # Move gray (5) pixels to bottom row, if not already there
    gray_pixels = find_pixels_by_color(input_grid,5)
    for r, c in gray_pixels:
        if r != bottom_row_index:
           output_grid[bottom_row_index,c] = 5
    

    return output_grid