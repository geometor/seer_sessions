"""
Double the input grid's dimensions, replicate gray pixels into 2x2 blocks, 
and create a checkered pattern of azure and white in specific rows and columns.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate Gray pixels into 2x2 blocks
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 5:
                output_grid[row*2, col*2] = 5
                output_grid[row*2+1, col*2] = 5
                output_grid[row*2, col*2+1] = 5
                output_grid[row*2+1, col*2+1] = 5

    # Fill Azure and White pattern
    for row in range(output_height):
      for col in range(output_width):
        if row % 2 == 0:  #even rows
          if col % 2 == 0:
            output_grid[row, col] = 8
          else:
            output_grid[row, col] = 0
        else:
          if output_grid[row,col] == 0:
            output_grid[row,col] = 0


    return output_grid