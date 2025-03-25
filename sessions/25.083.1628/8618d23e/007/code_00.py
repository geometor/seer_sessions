"""
Splits the input grid into two parts (top and bottom). The top part consists of rows that are uniform (all pixels in the row have the same value). The bottom part consists of the remaining rows.  Appends '9' to the end of each top part row. Inserts a single row of all 9s as a separator. Prepends '9' to the beginning of each bottom part row.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    in_rows, in_cols = input_grid.shape

    # Determine split point: Find the row where the row is NOT uniform.
    split_row = 0
    for i in range(in_rows):
        if not np.all(input_grid[i] == input_grid[i, 0]):
            split_row = i
            break
    
    if split_row == 0:  # If all rows are uniform, or there were no uniform rows, then NO split
        split_row = in_rows
        
    # Calculate output grid dimensions
    out_rows = in_rows + 1 # +1 for separator
    out_cols = in_cols + 1 # +1 for the appended/prepended 9

    # Initialize output grid
    output_grid = np.full((out_rows, out_cols), 9)

    # Process the top part
    output_row = 0
    for i in range(split_row):
        output_grid[output_row, :in_cols] = input_grid[i, :]
        output_row += 1

    # Add a full row of 9s as a separator
    #output_grid[output_row, :] = 9 #not necessary due to init

    #Process bottom part
    output_row = split_row+1
    for i in range(split_row, in_rows):
       output_grid[output_row, 1:in_cols+1] = input_grid[i,:]
       output_row += 1

    return output_grid.tolist()