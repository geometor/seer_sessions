"""
The transformation identifies a 2x2 subgrid at the top-left corner of the input grid. This subgrid's top-left corner aligns with the top-left corner of the input grid. The subgrid is then extracted and returned as the output.
"""

import numpy as np

def get_corner(input_grid):
    # Find top-left 2x2 subgrid
    for row in range(input_grid.shape[0] -1):
      for col in range(input_grid.shape[1]-1):
          if input_grid[row, col] != 0 and input_grid[row+1, col] != 0 :
                return row, col
    return 0, 0


def transform(input_grid):
    """
    Extracts the 2x2 subgrid at the top-left, limited by the non-zero pixels.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the top-left corner based on the color-alternation
    row, col = get_corner(input_grid)

    # Extract the 2x2 subgrid
    output_grid = input_grid[row:row+2, col:col+2]

    return output_grid.tolist()