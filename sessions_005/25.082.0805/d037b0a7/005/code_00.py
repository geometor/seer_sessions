"""
1.  **Identify Rightmost Non-zero Pixel:** For each row in the input grid, find the rightmost pixel that has a non-zero value.
2.  **Propagate Down and Left:** Starting from the identified pixel's position, propagate its value downwards to all subsequent rows in the same column.
3.  **Conditional Leftward Propagation:** In each row where the value was propagated downwards, propagate the value to the *left*, one cell at a time. Stop the leftward propagation when either:
    *   The beginning of the row is reached (column index 0).
    *   A cell with a non-zero value in the *original* input grid is encountered.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    for row_index in range(rows):
        # Find rightmost non-zero pixel
        rightmost_non_zero = None
        rightmost_col_index = -1
        for col_index in reversed(range(cols)):
            if input_grid[row_index, col_index] != 0:
                rightmost_non_zero = input_grid[row_index, col_index]
                rightmost_col_index = col_index
                break

        # Fill down and left if a rightmost non-zero pixel was found
        if rightmost_non_zero is not None:
            for lower_row_index in range(row_index + 1, rows):
                # Fill the cell in the same column
                output_grid[lower_row_index, rightmost_col_index] = rightmost_non_zero

                # Propagate to the left, checking against the ORIGINAL input_grid
                for fill_col_index in reversed(range(rightmost_col_index)):
                    if input_grid[lower_row_index, fill_col_index] != 0:
                        break  # Stop at first non-zero in the ORIGINAL grid
                    output_grid[lower_row_index, fill_col_index] = rightmost_non_zero

    return output_grid