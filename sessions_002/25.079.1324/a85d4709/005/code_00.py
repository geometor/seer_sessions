"""
The transformation rule involves replacing gray(5) cells in the input grid with either red(2), green(3), or yellow(4) based on their position relative to other gray cells. 0's will also be replaced.

1.  **Identify Gray Pixels:** Locate all cells in the input grid with the value 5 (gray). Also, keep track of 0 valued cells.
2.  **Check for Main Diagonal:** If all gray pixels are on the main diagonal (where the row index equals the column index), replace all gray pixels and all 0 pixels with red (2).
3.  **Check for Off-Diagonal:** If all gray pixels are on the off-diagonal (where the row index plus the column index equals the grid's dimension minus 1), replace all gray and 0 pixels with yellow (4).
4.  **Check for Lines:**
      * If all gray pixels are in the same row (but not a diagonal), replace with all gray and all 0 pixels green (3).
      * If all gray pixels are in the same column (but not a diagonal), replace with all gray and all 0 pixels green (3).
5.   **Otherwise:** If none of the above conditions are met, replace all gray pixels and all 0 pixels with yellow (4).
6.  **Output:** The modified grid is the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    gray_indices = np.where(input_grid == 5)
    zero_indices = np.where(input_grid == 0)
    row_indices = gray_indices[0]
    col_indices = gray_indices[1]

    # Check for Main Diagonal
    if np.all(row_indices == col_indices) and len(row_indices) > 0:
        output_grid[gray_indices] = 2
        output_grid[zero_indices] = 2
    # Check for Off-Diagonal
    elif np.all(row_indices + col_indices == rows - 1) and len(row_indices) > 0 :
        output_grid[gray_indices] = 4
        output_grid[zero_indices] = 4

    # Check for Lines
    elif (len(np.unique(row_indices)) == 1 and len(row_indices) > 0) or \
         (len(np.unique(col_indices)) == 1 and len(col_indices) > 0):
        output_grid[gray_indices] = 3
        output_grid[zero_indices] = 3
    # Otherwise
    elif len(row_indices) > 0:
        output_grid[gray_indices] = 4
        output_grid[zero_indices] = 4
    else:
       output_grid[zero_indices] = 0

    return output_grid.tolist()