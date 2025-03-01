"""
The transformation identifies the top-left object contains all non-zero colors, and extracts it into a new grid.
"""

import numpy as np

def get_top_left_object(grid):
    # Find the first row with non-zero element.
    rows_with_non_zero = np.any(grid != 0, axis=1)
    first_row = np.argmax(rows_with_non_zero)
  
    # Find the first column from this row.
    cols_with_non_zero = np.any(grid != 0, axis = 0)
    first_col = np.argmax(cols_with_non_zero)

    #find last row
    rows_with_non_zero_from_first = np.any(grid[first_row:, :] != 0, axis = 1)
    last_row = first_row + np.argmin(rows_with_non_zero_from_first)

    #find last col
    cols_with_non_zero_from_first = np.any(grid[:, first_col:] != 0, axis = 0)
    last_col = first_col + np.argmin(cols_with_non_zero_from_first)

    if first_row == last_row:
        last_row = first_row + 1
        for i in range(first_row + 1, len(grid)):
          if not np.any(grid[i,:] != 0, axis = 0):
            break;
          last_row = last_row + 1
    if first_col == last_col:
        last_col = first_col + 1
        for i in range(first_col + 1, len(grid[0,:])):
          if not np.any(grid[:,i] != 0, axis = 0):
            break;
          last_col = last_col + 1
    
    return first_row, first_col, last_row, last_col

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation.
    grid = np.array(input_grid)
    
    first_row, first_col, last_row, last_col = get_top_left_object(grid)

    # Extract the object
    output_grid = grid[first_row:last_row, first_col:last_col]

    return output_grid.tolist()