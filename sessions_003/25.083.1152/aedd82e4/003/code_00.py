"""
1.  **Copy the Input:** Create a copy of the input grid to serve as the output grid.
2.  **Column Rule (Bottom-Up):** Iterate through each column of the grid, starting from the *bottom* row and moving *upwards*.
    *   For each column, find the *last* (i.e., bottom-most) occurrence of a red pixel ('2').
    *   If a red pixel is found in that column, change its value to blue ('1') *in the output grid*.
3.  **Row Rule (Right-to-Left):** Iterate through each row of the *output* grid (which may have been modified by the column rule), starting from the *right-most* column and moving *left*.
    *   For each row, find the *last* (i.e., right-most) occurrence of a red pixel ('2'). Importantly, consider pixels that are *currently* red, including those that were originally red or turned red by previous operations within that row.
    *   If a red pixel is found in that row, change its value to blue ('1') in the output grid.
4. **Important Note:** The column rule is applied *before* the row rule. Changes made by the column rule affect the input to the row rule. The "last red" is determined at each rule individually.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Column Rule (Bottom-Up)
    for j in range(cols):
        last_red_row = -1
        for i in range(rows - 1, -1, -1):
            if output_grid[i, j] == 2:
                last_red_row = i
                break  # Find the *last* occurrence, then stop
        if last_red_row != -1:
            output_grid[last_red_row, j] = 1

    # Row Rule (Right-to-Left)
    for i in range(rows):
        last_red_col = -1
        for j in range(cols - 1, -1, -1):
            if output_grid[i, j] == 2:
                last_red_col = j
                break  # Find the *last* occurrence, then stop
        if last_red_col != -1:
            output_grid[i, last_red_col] = 1

    return output_grid