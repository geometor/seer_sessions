"""
Transforms a 9x9 input grid into a 4x4 output grid. The transformation involves
identifying a central vertical blue line, selecting two 2x4 regions on either
side, rotating each sub-grid, and combining them.
"""

import numpy as np

def get_vertical_line_index(grid):
    # Find the vertical line index
    rows, cols = grid.shape
    for j in range(cols):
      is_line = True
      if grid[0,j] != 1:
        is_line = False
      for i in range(1,rows):
        if grid[i,j] != 1:
          is_line=False
          break
      if is_line:
          return j

    return -1

def rotate_grid(grid):
    # Rotate a grid clockwise by 90 degrees.
    return np.rot90(grid, k=-1)

def transform(input_grid):
    """
    Transforms the input grid according to the defined rules.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the Central Line index
    line_index = get_vertical_line_index(input_grid)

    # 2. Define regions & 3.Select subgrids:
    # Define and select left subgrid
    left_subgrid = input_grid[0:4, 0:line_index]
    
    # Define and select right subgrid
    right_subgrid = input_grid[0:4, line_index + 1:cols]

    #4. Transpose the grids
    rotated_left = rotate_grid(left_subgrid)
    rotated_right = rotate_grid(right_subgrid)

    #5. Create and populate output grid
    output_grid = np.concatenate((rotated_right, rotated_left), axis=0)

    return output_grid.tolist()
