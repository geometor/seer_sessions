"""
The transformation identifies azure (8) pixels in the input grid. It copies these
azure pixels to the output grid. Then, for *some* of the azure pixels, it creates
a vertical line of green (3) pixels, extending upwards and downwards, with a total
length of four pixels.  Azure pixels at either extreme of the L shape are
unchanged.
"""

import numpy as np

def get_azure_pixels(grid):
    """Finds the coordinates of all azure (8) pixels in the grid."""
    return np.argwhere(grid == 8)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    azure_pixels = get_azure_pixels(input_grid)
    rows, cols = input_grid.shape

    for row, col in azure_pixels:
      # copy existing azure
        output_grid[row, col] = 8
      # grow green shoots up and down
        if 1<= row <= rows - 2:
                output_grid[row-1, col] = 3
                output_grid[row+1, col] = 3
        if 2<= row <= rows - 3:
                output_grid[row-2, col] = 3
                output_grid[row+2, col] = 3

    return output_grid