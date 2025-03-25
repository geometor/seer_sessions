"""
The transformation rule involves propagating colors downwards. The non-zero value in the top-right corner of the input grid is identified. Then, for each column, the algorithm checks for non-zero values. If a non-zero value is found, the algorithm propagates a specific value downwards, replacing zeros. The specific value propagated is the top right most non-zero value in the input grid.
"""

import numpy as np

def get_top_right_nonzero(grid):
    """Finds the top-right non zero value."""
    rows, cols = grid.shape
    for c in range(cols -1, -1, -1):
      for r in range(rows):
          if grid[r,c] != 0:
              return grid[r,c]

    return 0


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # identify top-right non-zero value
    fill_value = get_top_right_nonzero(input_grid)


    # Iterate through Columns
    for c in range(cols):
      # Iterate through Rows
      for r in range(rows):
            if output_grid[r,c] !=0:
                #Propagate fill_value down
                for r_below in range(r + 1,rows):
                    output_grid[r_below,c] = fill_value
            
    return output_grid