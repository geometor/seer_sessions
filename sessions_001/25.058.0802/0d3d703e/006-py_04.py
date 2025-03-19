"""
Increment each cell value in the input grid by 1, modulo 10. The output grid has the same shape as the input, preserving the spatial arrangement.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by adding 1 to each cell value, wrapping around to 0 if the result is 10.
    """
    # Initialize the output grid as a copy of the input grid.  Using numpy for easier manipulation.
    output_grid = np.array(input_grid).copy()

    # Iterate through each cell of the output grid and add 1 to its value.
    for row_index in range(output_grid.shape[0]):
        for col_index in range(output_grid.shape[1]):
            output_grid[row_index, col_index] = (output_grid[row_index, col_index] + 1) % 10

    return output_grid.tolist() # return as list