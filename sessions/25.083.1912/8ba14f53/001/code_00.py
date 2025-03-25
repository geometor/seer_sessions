"""
1.  **Identify Colored Blocks:** Examine the input grid. Note the distinct colored blocks separated/surrounded by '0' (white) pixels.
2.  **Get First Column and Transpose:** Get the first occurring color block. Transpose to fit in three rows.
3.  **Stack Alternating Colors with White:** In order, add a row of the transposed color, add a row of '0', and repeat for the remaining colors found.
"""

import numpy as np

def get_color_blocks(grid):
    """
    Identifies distinct colored blocks separated by '0's.
    Assumes rectangular blocks.  This is a simplification.
    """
    blocks = []
    first_col_color = None
    second_col_color = None

    #find first non-zero
    for x in range(grid.shape[1]):
      for y in range(grid.shape[0]):
        if grid[y,x] != 0:
          first_col_color = grid[y,x]
          break
      if first_col_color != None:
        break
    
    # find second non-zero
    for x in range(grid.shape[1]):
      for y in range(grid.shape[0]):
        if grid[y,x] != 0 and grid[y,x] != first_col_color:
          second_col_color = grid[y,x]
          break
      if second_col_color != None:
        break      

    blocks.append(first_col_color)
    blocks.append(second_col_color)

    return blocks, x

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    blocks, width = get_color_blocks(input_grid)
    output_grid = np.zeros((3, width), dtype=int)

    # Get first column
    first_color = blocks[0]
    second_color = blocks[1]

    # build the first color row
    for x in range(width):
      if input_grid[0,x] == first_color:
        output_grid[0,x] = first_color
      if input_grid[0,x] == 0:
        output_grid[0,x] = 0

    # build the second color row
    for x in range(width):
      if input_grid[0,x] == second_color:
        output_grid[1,x] = second_color
      if input_grid[0,x] == 0:
          output_grid[1,x] = 0          


    return output_grid.tolist()