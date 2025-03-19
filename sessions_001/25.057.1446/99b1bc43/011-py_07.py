"""
1.  **Determine Output Size:** The output grid will always have 4 columns. The number of rows in the output grid is the number of rows in the input grid divided by two using integer division.
2.  **Iterate Through Rows:** For each row in the input grid:
3.  **Check for Differences:** Compare the pixel in the last column of the current row with *every other* pixel in that same row.
4. **Mark Output**: If *any* of the pixels in the current row (excluding the last column) are different from the pixel in the last column, mark that row in the output. Set a value of 3 in the output grid, at column of the row's index divided by two (integer division) and row 0 if the input row is even, or column 3 and row input row index // 2 if input row index is odd.
5.  **Default Value:** If there are no differences detected in a row, set the value of the output row to 0. This is the default value if no changes are present.
"""

import numpy as np

def transform(input_grid):
    # Determine Output Size:  4 columns, rows = input rows // 2
    output_rows = input_grid.shape[0] // 2
    output_grid = np.zeros((output_rows, 4), dtype=int)

    # Iterate Through Rows
    for i in range(input_grid.shape[0]):
        # Check for Differences: Compare last column pixel with others in row
        last_col_val = input_grid[i, -1]
        row_changed = False
        for j in range(input_grid.shape[1] - 1):
            if input_grid[i, j] != last_col_val:
                row_changed = True
                break  # Exit inner loop as soon as a difference is found

        # Mark Output
        if row_changed:
            output_row = i // 2
            output_col = 0 if i % 2 == 0 else 3
            output_grid[output_row, output_col] = 3

    return output_grid