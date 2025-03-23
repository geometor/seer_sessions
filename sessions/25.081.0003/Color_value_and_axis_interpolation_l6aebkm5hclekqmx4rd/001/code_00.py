"""
Transforms an input grid by stacking rows from top to bottom onto the last row,
preserving non-zero values in the last row and filling zero positions with
values from upper rows sequentially.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through rows from top to bottom (excluding the last row)
    for i in range(rows - 1):
        # overlay row i onto all rows from i to rows-2, only filling zeros
        for j in range(cols):
          if input_grid[i, j] != 0:
            for k in range(i,rows-1):  #stack onto all rows up to last row.
              if output_grid[k,j] == 0:
                output_grid[k,j] = input_grid[i, j]

    return output_grid