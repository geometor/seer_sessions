"""
The transformation shifts non-zero elements upwards within each column of the input grid. Empty spaces created by the shift are filled with zeros at the bottom of the column. If a value would be shifted out of bounds it wraps to the bottom of the output grid for the same column it appeared in the input.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by shifting non-zero elements upwards within each column.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    num_rows, num_cols = input_grid.shape

    # Iterate through each column
    for j in range(num_cols):
        # Extract non-zero elements from the current column
        column = input_grid[:, j]
        non_zero_elements = column[column != 0]

        # Shift non-zero elements upwards with wrap-around
        num_non_zero = len(non_zero_elements)
        for i in range(num_rows):
          if i < num_non_zero:
            output_grid[i,j] = non_zero_elements[i]

    return output_grid.tolist()