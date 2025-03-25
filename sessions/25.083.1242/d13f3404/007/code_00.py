"""
The transformation rule replicates the input grid diagonally within the output grid. The output grid's dimensions are calculated by adding the number of rows and columns of the input grid and subtracting 1. The input grid slides diagonally, starting from the top-left corner of the output grid, and its content is copied at each step.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows + input_cols - 1
    output_cols = output_rows
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # iterate through diagonal offsets (sliding positions)
    for k in range(output_rows):
        # iterate through input grid cells
        for i in range(input_rows):
            for j in range(input_cols):
                # calculate output position with offset
                output_row = i + k
                output_col = j + k

                # check bounds
                if 0 <= output_row < output_rows and 0 <= output_col < output_cols:
                    # copy value
                    output_grid[output_row, output_col] = input_grid[i, j]

    return output_grid