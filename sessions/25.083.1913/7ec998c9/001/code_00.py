"""
Transforms an input grid by propagating the digit '1' from the left and top edges, stopping at non-'1' digits or the edges.  The propagation of '1' is determined by the existence and position of non-'1' pixels and the boundaries of the grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Locate non-1 digit (if any)
    non_one_indices = np.where(output_grid != 1)
    if non_one_indices[0].size > 0:
        # Check edges for propagation
        # Horizontal Propagation (Left to Right)
        for r in range(rows):
            for c in range(cols):
              if output_grid[r,c] != 1:
                break
              else:
                output_grid[r,c] = 1

        # Vertical Propagation (Top to Bottom)
        for c in range(cols):
            for r in range(rows):
              if output_grid[r,c] != 1:
                break
              else:
                output_grid[r, c] = 1

    # Fill first column and row, stopping at first original non 1 pixel if any
    non_1 = np.where(input_grid != 1)
    if (len(non_1[1]) > 0):
        min_col = min(non_1[1])
    else:
        min_col = cols

    if (len(non_1[0]) > 0):
        min_row = min(non_1[0])
    else:
        min_row = rows
      

    for j in range(min_col):
      output_grid[:, j] = np.where(input_grid[:,j] == 1, 1, 1)
    for i in range(min_row):
      output_grid[i, :] = np.where(input_grid[i,:] == 1, 1, 1)


    return output_grid