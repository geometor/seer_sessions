"""
The transformation rule involves two primary actions:

1.  First Row Transformation: The first row of the input grid is always changed to gray (color code 5) in the output grid, regardless of the original colors in the input.
2.  Other Rows Transformation: All rows below the first row are transformed to white (color code 0) in the output grid, irrespective of their initial colors.
3.  Shape Preservation: The dimensions (height and width) of the grid remain unchanged throughout the process.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input, filled with white (0).
    output_grid = np.zeros_like(input_grid)

    # Transform the first row to gray (5).
    output_grid[0, :] = 5

    # All other rows are already white (0) due to the initialization.

    return output_grid