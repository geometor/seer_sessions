"""
1.  **Identify the Key Column:** Find the column in the input grid that consistently contains the digit '1' (blue).
2.  **Extract Output Grid:** Create a new grid. The height is the same as the input. The width is always 3.
3.  **Populate values:** For each row in the input
    *   Locate the key column (value of '1')
    *   If a cell is in same row and is one column to the left, same column, or one column to the right relative to the key column
        * set the coresponding cell in the output to be '3' (green)
    *   Otherwise
        *   set value to '0' (white)
"""

import numpy as np

def find_key_column(grid):
    # Find the column index that contains the value 1
    for j in range(grid.shape[1]):
        if 1 in grid[:, j]:
            return j
    return -1  # Should not happen based on problem description, but good practice

def transform(input_grid):
    # initialize output_grid
    rows = input_grid.shape[0]
    cols = 3
    output_grid = np.zeros((rows, cols), dtype=int)
    
    # Find the key column
    key_column_index = find_key_column(input_grid)

    # change output pixels
    for i in range(rows):
        for j in range(cols):
            # calculate input grid column
            input_col = key_column_index + j -1
            
            # Check boundaries for input grid
            if 0 <= input_col < input_grid.shape[1]:
                output_grid[i,j] = 3
            else:
                output_grid[i,j] = 0


    return output_grid