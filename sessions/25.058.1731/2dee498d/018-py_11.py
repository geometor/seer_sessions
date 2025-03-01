"""
The transformation extracts the first two columns of the input grid to form the output grid. The output grid has the same height as the input grid but a fixed width of 2.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same number of rows as the input and 2 columns.
    output_grid = np.empty((input_grid.shape[0], 2), dtype=int)

    # Copy the first two columns from the input grid to the output grid.
    output_grid[:, 0] = input_grid[:, 0]
    output_grid[:, 1] = input_grid[:, 1]

    return output_grid