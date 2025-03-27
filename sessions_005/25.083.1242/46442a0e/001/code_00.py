"""
The transformation takes the input grid, doubles it dimensions, flips the rows to create new rows and builds the output grid by concatenating the new rows with the original rows, doubling the number of times the rows are repeated to match the new dimensions.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_np = np.array(input_grid)
    rows, cols = input_np.shape
    output_rows = rows * 2
    output_cols = cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Flip the order of the rows of the original.
    flipped_rows = np.flip(input_np, axis=0)

    # Concatenate the original input rows with the flipped input rows.
    concatenated_rows = np.concatenate((input_np, flipped_rows), axis=1)

    #build output by repeating concatenated rows
    for i in range(rows):
      output_grid[i] = concatenated_rows[i]
      output_grid[i + rows] = concatenated_rows[rows - 1 - i]


    return output_grid.tolist()