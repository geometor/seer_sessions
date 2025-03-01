"""
The transformation rule is to change the color of the maroon (9) object located at the bottom-right of the input grid to grey (5) in the output grid. All other objects and their positions remain unchanged.
"""

import numpy as np

def find_object_by_color(grid, color):
    # Find the coordinates of all pixels with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Object of specified color not found

    # bounding box
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])

    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the maroon object (color 9).
    maroon_object_coords = find_object_by_color(input_grid, 9)

    # If a maroon object is found, change its color to grey (5).
    if maroon_object_coords:
        min_row, max_row, min_col, max_col = maroon_object_coords
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if output_grid[row, col] == 9:  # ensure we are changing correct cells
                  output_grid[row, col] = 5

    return output_grid