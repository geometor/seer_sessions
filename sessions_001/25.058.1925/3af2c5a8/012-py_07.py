"""
1. **Expansion:** Double the dimensions of the input grid to create an output grid.
2. **Replication:** For each pixel in the input grid, create a 2x2 block of the same color in the output grid. Specifically, `output_grid[2*i, 2*j]`, `output_grid[2*i+1, 2*j]`, `output_grid[2*i, 2*j+1]`, and `output_grid[2*i+1, 2*j+1]` all receive the value of `input_grid[i, j]`.
3. **Selective Inversion**: Iterate through each cell in the *output* grid.
   * If a cell's value is 3, change it to 0.
   * If a cell's value is 0, change it to 3.
   * Otherwise, leave cell value unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # replicate and insert rows and columns
    for i in range(input_height):
        for j in range(input_width):
            output_grid[2*i, 2*j] = input_grid[i, j]
            output_grid[2*i+1, 2*j] = input_grid[i, j]
            output_grid[2*i, 2*j+1] = input_grid[i, j]
            output_grid[2*i+1, 2*j+1] = input_grid[i, j]
    
    # selective inversion of 0 and 3, otherwise leave unchanged
    for i in range(output_height):
      for j in range(output_width):
        if output_grid[i,j] == 3:
           output_grid[i,j] = 0
        elif output_grid[i,j] == 0:
           output_grid[i,j] = 3

    return output_grid