"""
Transforms an input grid by identifying a single non-zero pixel and generating a vertical line of '4's (yellow) above it. The length of the yellow line is determined by the row index of the non-zero pixel. The rest of the grid remains unchanged (filled with 0s).
"""

import numpy as np

def find_nonzero_pixel(grid):
    """Finds the coordinates of the single non-zero pixel in the grid."""
    non_zero_indices = np.nonzero(grid)
    if len(non_zero_indices[0]) > 0:
        return non_zero_indices[0][0], non_zero_indices[1][0]  # row, col
    else:
        return None  # Or raise an exception, if it should always exist

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the non-zero pixel
    nonzero_pixel_coords = find_nonzero_pixel(input_grid)

    if nonzero_pixel_coords is None:
      return output_grid

    row, col = nonzero_pixel_coords
    
    # Generate the vertical line of 4s.
    for i in range(row):
        output_grid[i, col] = 4

    return output_grid