"""
Examine each column of the input grid.
Identify columns containing the color '2' (red).
Remove all columns from the grid that include 2(red).
Construct the output grid by keeping all rows and the remaining columns, preserving their original order from left to right.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing columns containing the color '2' (red).
    """
    input_grid = np.array(input_grid)
    num_rows, num_cols = input_grid.shape
    output_cols = []

    # Iterate through each column of the input grid
    for j in range(num_cols):
        column = input_grid[:, j]
        # Check if the color '2' is present in the column
        if 2 not in column:
            output_cols.append(column)

    # Construct the output grid from the selected columns
    if len(output_cols) > 0 :
      output_grid = np.stack(output_cols, axis=1)
    else:
      output_grid = np.array([])

    return output_grid.tolist()