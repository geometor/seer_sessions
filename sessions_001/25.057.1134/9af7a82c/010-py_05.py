"""
The transformation operates on each column independently. The output grid's height
is the input height + the number of rows in the input.  The top cell of each output
column is filled with color 2 (red). The remaining colors from the corresponding
input column are placed in the output column, shifted down by one position.
Empty spaces are left as color 0.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_height = input_grid.shape[0] + input_grid.shape[0] # input_height + input_rows
    output_grid = np.zeros((output_height, input_grid.shape[1]), dtype=int)

    # change output pixels
    for j in range(input_grid.shape[1]):
        # Place color 2 at the top of each column
        output_grid[0, j] = 2

        # Shift the input column down by one position in the output column
        for i in range(input_grid.shape[0]):
            output_grid[i + 1, j] = input_grid[i, j]

    return output_grid