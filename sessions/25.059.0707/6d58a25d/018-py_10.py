"""
1. Change all yellow (4) pixels to green (3).
2. Identify all green (3) pixels (including the newly changed ones).
3. Find the columns that contain any green (3) pixels.
4. Fill all cells in those columns with green (3).
"""

import numpy as np

def get_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)

    # Change yellow pixels to green.
    yellow_pixels = get_pixels_by_color(input_grid, 4)
    for r, c in yellow_pixels:
        output_grid[r, c] = 3

    # Find columns with green pixels (including newly changed).
    green_pixels = get_pixels_by_color(output_grid, 3)  # Use output_grid here
    green_columns = np.unique(green_pixels[:, 1])

    # Fill those columns with green.
    rows, cols = output_grid.shape
    for c in green_columns:
        for r in range(rows):
            output_grid[r, c] = 3

    return output_grid