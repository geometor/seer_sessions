"""
The program inserts a '6' before columns that contain a yellow pixel and are immediately to the right of an all-white column.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]
    output_grid = output_grid.tolist()

    # Iterate through columns
    for j in range(cols):
        #Check if the left neightbor column is all white
        if j > 0:
          all_white = True
          for i in range(rows):
            if input_grid[i][j-1] != 0:
              all_white = False
              break
          if all_white:
            # Check this column for yellows, if so then prepend a 6 to this column
            for i in range(rows):
              if input_grid[i][j] == 4:
                  output_grid[i][j] = 6
                  break;

    return np.array(output_grid)