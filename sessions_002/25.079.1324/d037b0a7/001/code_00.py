"""
The program iterates through each row of the input grid. For each row, it identifies the value in the last column. 
It then fills the output grid's corresponding row by replacing 0 values with the value from the input grid's last column of the same row.
If there exists cells in the current input row that are not zero and not equals to the right most value, 
these cell remains in the output but also will fill to the cells below it.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions and data type as the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for i in range(rows):
        # Identify the value in the last column of the current input row
        last_col_val = input_grid[i, -1]
        
        # Iterate through each cell in current row
        for j in range(cols):
            # fill the cells below with the previous non-zero cell
            if input_grid[i,j] != 0 and input_grid[i,j] != last_col_val:
                output_grid[i,j] = input_grid[i,j]
                for k in range(i + 1, rows):
                    output_grid[k,j] = output_grid[i,j]

            # If the last column value is not zero, set the cell value
            if last_col_val != 0 and input_grid[i,j] == 0:
                output_grid[i, j] = last_col_val
            
    return output_grid