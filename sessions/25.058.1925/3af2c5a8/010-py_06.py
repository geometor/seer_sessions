"""
The input grid is expanded to double its original height and width. Each row and column in the input is replicated into two of the same in the output. The replicated grid creates a checkerboard effect, surrounded by inverse.
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
    
    # create inverse checkerboard
    for i in range(output_height):
      for j in range(output_width):
        if (i + j) % 2 == 1:
          if output_grid[i,j] == 3:
             output_grid[i,j] = 0
          elif output_grid[i,j] == 0:
             output_grid[i,j] = 3

    return output_grid