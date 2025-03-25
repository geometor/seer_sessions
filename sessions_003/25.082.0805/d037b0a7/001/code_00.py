"""
The function identifies the rightmost non-zero pixel in each row of the input grid and uses its value to fill cells below it, in subsequent rows and to the left up to the column index of the rightmost non-zero pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    for row_index in range(rows):
        # Find rightmost non-zero pixel
        rightmost_non_zero = None
        rightmost_col_index = -1
        for col_index in reversed(range(cols)):
            if output_grid[row_index, col_index] != 0:
                rightmost_non_zero = output_grid[row_index, col_index]
                rightmost_col_index = col_index
                break

        # Fill down if a rightmost non-zero pixel was found
        if rightmost_non_zero is not None:
            for lower_row_index in range(row_index + 1, rows):
                for fill_col_index in range(rightmost_col_index + 1):
                  output_grid[lower_row_index, fill_col_index] = rightmost_non_zero

    return output_grid