"""
1.  **Identify the Gray Column:** Locate the column in the input grid that contains the color gray (value 5).
2.  **Create output grid:** Create output grid size of input grid height and a constant of 3 columns wide.
3.  **Transform to Red:** Replace that entire output column to the color red (value 2).
4.  **Fill Remaining with white:** Fill the remaining columns of output with the color white (value 0).
"""

import numpy as np

def find_gray_column(grid):
    # Iterate through columns to find the one containing gray (5)
    for j in range(grid.shape[1]):
        if 5 in grid[:, j]:
            return j
    return -1  # Return -1 if no gray column is found

def transform(input_grid):
    # Create output grid of the same height and 3 width, filled with white (0)
    output_grid = np.zeros((input_grid.shape[0], 3), dtype=int)

    # Find the index of gray column
    gray_column_index = find_gray_column(input_grid)
    
    # if gray_column exists, then we turn index 1 to red
    if gray_column_index != -1:
        output_grid[:, 1] = 2

    return output_grid