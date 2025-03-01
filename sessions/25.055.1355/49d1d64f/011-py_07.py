"""
The transformation appends a copy of the last column of the input. After that it
duplicates each row of the intermediate grid to form the final output.
"""

import numpy as np

def transform(input_grid):
    # Append a copy of the last column to the input grid.
    last_column = input_grid[:, -1:]
    intermediate_grid = np.concatenate((input_grid, last_column), axis=1)

    # Duplicate each row of the intermediate grid.
    output_grid = np.concatenate((intermediate_grid, intermediate_grid), axis=0)

    return output_grid