"""
Identify the single non-zero pixel in the input grid.  Change the color of this pixel from blue (1) to red (2). Move the pixel from its original location to the top-left corner (0, 0).  All other pixels remain white (0).
"""

import numpy as np

def find_non_zero_pixel(grid):
    """Finds the coordinates of the non-zero pixel in a grid."""
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 0:
                return (i, j)
    return None  # Should not happen in this specific task, but good practice

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    # Initialize output grid with all zeros and same dimensions as input
    output_grid = np.zeros_like(input_grid)

    # Find the non-zero pixel in the input grid
    non_zero_pixel_coords = find_non_zero_pixel(input_grid)

    # if non zero pixel exists, put a red pixel in the top left
    if non_zero_pixel_coords:
      output_grid[0, 0] = 2

    return output_grid