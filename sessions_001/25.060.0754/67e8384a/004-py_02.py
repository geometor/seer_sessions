"""
The input grid is mirrored along both its horizontal and vertical axes to create the output grid. The center of each grid remains in the center after the transformations.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # Reflect Horizontally
    for i in range(rows):
      for j in range(cols):
        output_grid[i,j] = input_grid[i,j]
        output_grid[i, 2*cols - 1 - j] = input_grid[i,j]

    # Reflect Vertically
    for i in range(rows):
      for j in range(2 * cols):
        output_grid[2*rows - 1 - i, j] = output_grid[i,j]

    return output_grid.tolist()