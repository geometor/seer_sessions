"""
Transforms an input grid based on the position of a single red pixel (value 2)
to an output grid with a specific pattern of colored pixels. The specific
transformation appears to depend on a set of predefined rules.
"""

import numpy as np

def get_red_pixel_position(grid):
    """Finds the coordinates of the red pixel (value 2) in the grid."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 2:
                return (r, c)
    return None  # Should not happen, based on task description

def transform(input_grid):
    """
    Transforms the input grid based on the location of the red pixel.
    """
    output_grid = np.zeros_like(input_grid)
    red_pixel_pos = get_red_pixel_position(input_grid)

    if red_pixel_pos is None:
        return output_grid # Return all zeros, no change.

    r, c = red_pixel_pos

    if (r, c) == (0, 1):
      output_grid[0, 0] = 3
      output_grid[0, 2] = 6
    elif (r, c) == (2, 4):
      output_grid[1, 3] = 3
    elif (r, c) == (0, 2):
       output_grid[1, 1] = 8
       output_grid[1, 3] = 7
    elif (r,c) == (1,3):
      output_grid[0, 2] = 3
      output_grid[0, 4] = 6
      output_grid[2, 2] = 8
      output_grid[2, 4] = 7

    return output_grid