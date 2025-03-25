"""
The transformation takes each column of the input grid and uses it to create rows in the output grid, starting with the last row.  Specifically:

1.  The first column of the input grid becomes the *last* row of the output grid.
2.  The second column of the input grid becomes the *second-to-last* row of the output grid.
3.  The third column of the input grid becomes the *first* row of the output grid.
4.  This pattern continues for any number of columns: the *nth* column in the input becomes the *n*th to last row in the output.  The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by mapping input columns to output rows in reverse order.
    """
    input_array = np.array(input_grid)
    num_rows, num_cols = input_array.shape
    output_grid = np.zeros((num_rows, num_cols), dtype=int)  # Initialize with correct dimensions

    # Iterate through columns of the input
    for j in range(num_cols):
        # Get the current column
        column = input_array[:, j]
        # Place the column into the appropriate row of the output (in reversed order)
        output_grid[num_rows - 1 - j, :] = column

    return output_grid.tolist()