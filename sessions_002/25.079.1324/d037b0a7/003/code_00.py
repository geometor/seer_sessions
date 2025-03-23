"""
1.  **Identify Key Values:** For each row in the input grid, identify two key values:
    *   The value in the last column of that row (the "last column value").
    *   Any non-zero values in the row *that are not equal to* to the "last column value"

2.  **Initial Fill:**
    *   Copy the input to output
    *   Iterate each row, if a cell is equal to zero *and* the last column value
        is not zero, replace the zero with the last column value

3.  **Conditional Downward Propagation, phase 1:** For each row, iterate through each cell. If a cell's value is non-zero and is *not* equal to the last column value, then:

    * fill that value down entire column

4.  **Conditional Downward Propagation, phase 2:**
    * starting at row 0, find the last column value
    * if the last column value in the current row is not zero
      - continue down the column, replacing any zeros with that value, until a non-zero value is reached
      - repeat for each row
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions and data type as the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row (Initial Fill and identify key values)
    for i in range(rows):
        last_col_val = input_grid[i, -1]  # "last column value"

        # fill zero cells with last_col_val
        for j in range(cols):
           if last_col_val != 0 and input_grid[i,j] == 0:
                output_grid[i, j] = last_col_val
        
    # Conditional Downward Propagation, phase 1
    for i in range(rows):
        last_col_val = input_grid[i, -1]
        for j in range(cols):
            if output_grid[i,j] != 0 and output_grid[i,j] != last_col_val:
                for k in range(i, rows):
                    output_grid[k,j] = output_grid[i,j]

    # Conditional Downward Propagation, phase 2
    for i in range(rows):
        last_col_val = input_grid[i,-1]
        if last_col_val != 0:
            for k in range(i, rows):
                if output_grid[k, -1] == 0:
                    output_grid[k, -1] = last_col_val
                else:
                    break # stop if we see a non-zero

    return output_grid