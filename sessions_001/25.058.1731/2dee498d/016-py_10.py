"""
The transformation takes the input grid and selects the first two columns to form the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the appropriate dimensions.
    # The output grid has the same number of rows as the input,
    # and the number of colums is set to two
    output_grid = np.empty((input_grid.shape[0], 2), dtype=int)

    # Select first two columns
    output_grid[:, 0] = input_grid[:, 0]
    output_grid[:, 1] = input_grid[:, 1]
   

    return output_grid