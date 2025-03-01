"""
Expands the input grid, replicates yellow pixels, and fills the remaining space with azure in a mirrored pattern.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # 1. Expand the Grid: Double the dimensions (approximately).
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 2. Replicate Yellow Pixels and 3. Fill
    for i in range(input_height):
        for j in range(input_width):
            if input_grid[i, j] == 4:
                # Original position
                output_grid[i, j] = 4
                # Mirrored position
                output_grid[i, j + input_width] = 4

    # iterate again with the expanded grid
    for i in range(output_height):
      for j in range(output_width):
        if output_grid[i,j] == 0:
          # left
          if j < output_width / 2:
            output_grid[i,j] = output_grid[i, output_width-1-j]
          # right
          if j >= output_width /2:
             output_grid[i,j] = output_grid[i, output_width-1-j]

          if output_grid[i,j] == 0:
            output_grid[i,j] = 8


    return output_grid