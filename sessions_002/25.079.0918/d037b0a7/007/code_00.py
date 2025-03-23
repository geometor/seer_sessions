"""
The transformation rule for each column can be described as follows:

For each column:

1.  **Check First Row:** If the cell in the first row of the current column has a non-zero value, copy this value to all cells in that column.
2.  **If First Row is Zero:** If the cell in the first row of the current column is zero, iterate through the remaining rows of the column (starting from the second row). For each cell, copy the value from the cell directly above it in the same column.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each column
    for j in range(cols):
        # Check the first row of the current column
        first_row_value = output_grid[0, j]

        if first_row_value != 0:
            # Copy the first row value to all cells in the column
            for i in range(rows):
                output_grid[i, j] = first_row_value
        else:
            # Iterate through the remaining rows and copy from above
            for i in range(1, rows):
                output_grid[i, j] = output_grid[i - 1, j]

    return output_grid