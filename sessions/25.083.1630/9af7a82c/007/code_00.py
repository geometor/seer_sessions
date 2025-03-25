"""
1.  **Reverse Each Row:** Reverse the order of elements within each row of the input grid.

2.  **Create Output Grid:**
    *   The output grid will have a number of columns equal to the number of columns in the input grid plus one.
    *   The output grid will have a number of rows equal to 5 if the number of input rows is less than or equal 5, otherwise 6.

3.  **Populate First Column:** The first column of the output grid is populated with the last element of each input row, taken in order. If the output has more rows then the input, the remaining cells of the first column are filled with 0.

4.  **Populate Remaining Columns:** Starting from the second column of the output grid, populate each row with the reversed elements of the corresponding input row, *excluding* the last element (which is already in the first column).

5.  **Padding:** If any cells in the output grid remain empty after steps 3 and 4, fill them with 0 (white). This happens:
    *   In the first column when input rows are less than output rows.
    *   In any row where the input row has fewer elements than the output row length
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = 5 if rows <= 5 else 6
    output_cols = cols + 1
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # populate first column of output
    for i in range(rows):
        output_grid[i, 0] = input_grid[i, -1]

    # populate other columns
    for i in range(rows):
        reversed_row = input_grid[i, :-1][::-1]  # Reverse without the last element
        for j in range(len(reversed_row)):
            output_grid[i, j + 1] = reversed_row[j]

    return output_grid