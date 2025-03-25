"""
1.  **Find the Key Column:** Scan the input grid to identify the column index containing the value '1' (blue). This is the "key column."

2.  **Create Output Grid:** Create a new output grid. The output grid has the same number of rows as the input grid, but its width is always 3 columns.

3.  **Populate Output Grid Rows:** Iterate through each row of the input grid. For each row:
    *   Check the cell one position to the left of the key column. If the value is not 0, place a '3' (green) in the first column (index 0) of the output grid for that row. Otherwise if out-of-bounds or 0, set value to 0.
    *   Check the cell in the key column. If the input value is 1, place '3' (green) in the second column (index 1) of the output grid for that row. Otherwise, set to 0.
    *   Check the cell one position to the right of the key column. If the input cell is within bounds and the value is not 0, place a '3' (green) in the third column (index 2) of the output grid for that row. Otherwise if out-of-bounds or 0, set value to 0.
    * if none of the above condtions are met, output grid values for the coresponding rows are 0.
"""

import numpy as np

def find_key_column(grid):
    # Find the column index that contains the value 1
    for j in range(grid.shape[1]):
        if 1 in grid[:, j]:
            return j
    return -1  # Should not happen

def transform(input_grid):
    # initialize output_grid
    rows = input_grid.shape[0]
    cols = 3
    output_grid = np.zeros((rows, cols), dtype=int)
    
    # Find the key column
    key_column_index = find_key_column(input_grid)

    # Populate output_grid
    for i in range(rows):
        # Left of key column
        input_col = key_column_index - 1
        if 0 <= input_col < input_grid.shape[1] and input_grid[i, input_col] != 0:
            output_grid[i, 0] = 3
        else:
            output_grid[i, 0] = 0

        # At key column
        input_col = key_column_index
        if 0 <= input_col < input_grid.shape[1] and input_grid[i, input_col] == 1:
            output_grid[i, 1] = 3
        else:
            output_grid[i,1] = 0

        # Right of key column
        input_col = key_column_index + 1
        if 0 <= input_col < input_grid.shape[1] and input_grid[i, input_col] != 0:
            output_grid[i, 2] = 3
        else:
            output_grid[i,2] = 0


    return output_grid