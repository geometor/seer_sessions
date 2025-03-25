"""
The transformation rule involves counting non-zero pixels in each column of the input grid and then vertically stacking that many non-zero pixels in the corresponding column of the output grid, starting from the top row. The values of the stacked pixels are taken from the non zero values in the input, filling up the column top down and left to right.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described vertical stacking logic.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column of the input grid
    for c in range(cols):
        # Count non-zero pixels in the current column
        non_zero_count = np.count_nonzero(input_grid[:, c])

        # Extract non-zero values from the input grid, column-wise, then row-wise
        non_zero_values = []
        for input_c in range(cols):
          for input_r in range(rows):
            if input_grid[input_r, input_c] != 0:
              non_zero_values.append(input_grid[input_r,input_c])

        # Stack the non-zero values vertically in the output grid
        for r in range(min(non_zero_count, rows)):
            output_grid[r, c] = non_zero_values[r] if r < len(non_zero_values) else 0

    return output_grid.tolist()