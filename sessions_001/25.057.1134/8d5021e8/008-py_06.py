"""
Expands the input grid into a 9x4 output grid, replicating a pattern and adding white lines.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as 9x4 filled with red (2)
    output_grid = np.full((9, 4), 2)

    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Place white (0) in the first and last columns
    output_grid[:, 0] = 0
    output_grid[:, 3] = 0
    
    # Find white pixels in input
    white_pixels = np.argwhere(input_grid == 0)

    # Iterate through white pixels and perform expansion and placement of the white
    for r, c in white_pixels:
      if r - 1 >=0:
        output_grid[r*3, c*3] = 0
      output_grid[r*3 + 2, c * 3] = 0
      output_grid[r*3 + 3, c*3] = 0

    return output_grid