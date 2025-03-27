"""
Examine every other column of the input, starting with the second column containing a non-zero value.
Within those columns, take the values of every other row, starting with the first row.
Construct the output grid from those values.
"""

import numpy as np

def get_non_zero_columns(input_grid):
    """
    Returns a list of indices of columns that contain non-zero values.
    """
    non_zero_columns = []
    for j in range(input_grid.shape[1]):
        if np.any(input_grid[:, j] != 0):
            non_zero_columns.append(j)
    return non_zero_columns

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the second column with a non-zero value
    non_zero_cols = get_non_zero_columns(input_grid)
    start_col = non_zero_cols[1] if len(non_zero_cols) > 1 else (non_zero_cols[0] if len(non_zero_cols) >0 else 0 )

    # Determine dimensions of output
    output_height = (input_grid.shape[0] + 1) // 2
    
    output_width = 0
    for j in range(start_col, input_grid.shape[1], 2):
       output_width +=1
    
    # Initialize output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Extract values
    output_row = 0
    output_col = 0    
    for j in range(start_col, input_grid.shape[1], 2):
      output_row = 0
      for i in range(0, input_grid.shape[0], 2):        
            output_grid[output_row, output_col] = input_grid[i, j]
            output_row += 1
      output_col +=1
    return output_grid.tolist()