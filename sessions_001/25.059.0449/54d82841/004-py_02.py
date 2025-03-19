"""
1.  **Identify Columns with Magenta:** Scan the input grid and identify all columns that contain one or more magenta (6) pixels.
2.  **Transform Bottom Row:** For each column identified in step 1, change the pixel in the last row of that column to yellow (4).
3.  **Preserve Other Pixels:** All other pixels in the grid remain unchanged.
"""

import numpy as np

def get_columns_with_color(grid, color):
    """
    Finds the indices of columns containing at least one pixel of the specified color.
    """
    cols = []
    for col in range(grid.shape[1]):
        if np.any(grid[:, col] == color):
            cols.append(col)
    return cols

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule:
    - Identifies columns with magenta pixels.
    - Changes the bottom-row pixel in those columns to yellow.
    - Keeps all other pixels the same.
    """
    output_grid = np.copy(input_grid)
    magenta_cols = get_columns_with_color(input_grid, 6)

    # Change the last row's pixels in the identified columns to yellow
    for col in magenta_cols:
        output_grid[-1, col] = 4

    return output_grid