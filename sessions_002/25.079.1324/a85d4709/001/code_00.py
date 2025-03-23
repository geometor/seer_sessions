"""
The transformation rule involves replacing gray(5) cells in the input grid with either red(2), green(3), or yellow(4) based on their position relative to other gray cells, all 0's will also be replaced.

1.  **Identify 5s:** Locate all cells in the input grid with the value 5 (gray).
2.  **Replacement Rule:**
    *   If 5's are found, determine output color:
        *   If gray's are only in one row or column, replace all cells with 3 (green)
        *   Otherwise:
            *   If gray is in diagonal (row index = column index) replace all cells with 2 (red)
            *   If gray is in any other configuration replace all cells with 4 (yellow).
3.  **Output:** The modified grid is the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find rows and columns containing 5
    rows_with_5 = np.any(input_grid == 5, axis=1)
    cols_with_5 = np.any(input_grid == 5, axis=0)
    num_rows_with_5 = np.sum(rows_with_5)
    num_cols_with_5 = np.sum(cols_with_5)
   
    # Determine replacement color
    if num_rows_with_5 == 1 or num_cols_with_5 == 1:
        replacement_color = 3  # Green
    else:

        gray_indices = np.where(input_grid == 5)
        
        row_indices = gray_indices[0]
        col_indices = gray_indices[1]

        if all(row_indices == col_indices):
          replacement_color = 2
        else:
          replacement_color = 4


    output_grid[:] = replacement_color

    return output_grid.tolist()