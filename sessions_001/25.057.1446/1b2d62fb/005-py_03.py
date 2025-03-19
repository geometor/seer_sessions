"""
1.  **Identify Input Objects:** Find all blue (value 1) pixels in the input grid.
2.  **Record Column Positions:** Note the column index of each blue pixel.
3.  **Order Columns:** Sort these column indices in *descending* order.
4. **Determine Output Rows** Create an output grid with the same number of rows
    as the input grid and a fixed width of 3. The sorted column indices from
    step 3 determine *which rows in the output will have azure.*
5.  **Place Azure Pixels:** For each column index (now representing a *row* index
    in the output), place an azure (value 8) pixel.
    The position of the azure pixel within each row follows this rule:
    -The row index in the **sorted** list corresponds to the column index of the azure pixel.
6.  **All Other Pixels:** All other pixels in the output grid remain black (value 0).
"""

import numpy as np

def get_blue_columns(grid):
    # Find columns containing blue (1) pixels
    blue_columns = []
    for col in range(grid.shape[1]):
        if np.any(grid[:, col] == 1):
            blue_columns.append(col)
    return blue_columns

def transform(input_grid):
    # initialize output_grid to all zeros, same height as input, width 3
    output_grid = np.zeros((input_grid.shape[0], 3), dtype=int)

    # Find the columns in input that contain blue pixels
    blue_cols = get_blue_columns(input_grid)

    # Sort the columns in descending order
    sorted_cols = sorted(blue_cols, reverse=True)
    
    # place azure pixel in each output row 
    for i, col in enumerate(sorted_cols):
        if i < output_grid.shape[0]: # ensure we do not exceed bounds
          output_grid[col, i] = 8


    return output_grid