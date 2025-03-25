```python
"""
1.  **Iterate through Rows:** Process each row of the input grid sequentially, from top to bottom.
2.  **Find Rightmost Non-zero Pixel:** In the current row, identify the rightmost pixel with a non-zero value.
3.  **Propagate Downwards:** If a rightmost non-zero pixel is found, copy its value to all cells directly below it in the same column, for all subsequent rows.
4.  **Conditional Leftward Propogation:**
    For each row *below* the one where the rightmost non-zero pixel was originally found, check the cell filled in by propagation down.
    Propagate *that* value to the left one at at time stopping if:
        The beginning of the row is reached.
        A non-zero pixel exists in the original input grid
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
```