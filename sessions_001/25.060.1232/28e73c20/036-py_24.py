"""
1.  **Examine Input Dimensions:** Determine the number of rows and columns in the input grid.
2.  **Conditional Border:** If *either* the number of rows *or* the number of columns is even, create a green (value 3) border around the grid. The border consists of filling the outermost rows and columns with green.
3.  **Conditional Cross:** If *both* the number of rows *and* the number of columns are odd, create a green (value 3) cross at the center of the grid. The cross consists of filling the central row(s) and central column(s) with green. If the number of rows is even, there are two central rows. Similarly, if the number of columns is even, there are two central columns.
4.  **Output:** The result will be a copy of input grid with either a border or a cross, not both.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros (white), then copy the input grid to the output
    output_grid = np.zeros_like(input_grid)
    output_grid[:] = input_grid

    rows, cols = output_grid.shape

    # Conditional Border
    if rows % 2 == 0 or cols % 2 == 0:
        # Create the border (fill outermost rows and columns with green)
        output_grid[0, :] = 3
        output_grid[rows - 1, :] = 3
        output_grid[:, 0] = 3
        output_grid[:, cols - 1] = 3
    # Conditional Cross
    elif rows % 2 != 0 and cols % 2 != 0:
        # Find the central row(s) and column(s)
        if rows % 2 == 0:  # Even number of rows
            center_rows = [rows // 2 - 1, rows // 2]
        else:  # Odd number of rows
            center_rows = [rows // 2]

        if cols % 2 == 0:  # Even number of columns
            center_cols = [cols // 2 - 1, cols // 2]
        else:  # Odd number of columns
            center_cols = [cols // 2]

        # Fill the central row(s) and column(s) with green
        for r in center_rows:
            for c in range(cols):  # Iterate through all columns
                output_grid[r, c] = 3
        for c in center_cols:
            for r in range(rows):  # Iterate through all rows
                output_grid[r, c] = 3

    return output_grid