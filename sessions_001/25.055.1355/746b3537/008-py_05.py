"""
The transformation extracts the top row of the input grid and creates a new grid with that row. The height of output is one, and the width of the output is the same as the width of the input. The values and their order in the selected row are preserved.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Initialize the output grid with dimensions 1 x cols.
    output_grid = np.zeros((1, cols), dtype=int)

    # Copy the first row of the input grid to the output grid.
    output_grid[0, :] = input_grid[0, :]

    return output_grid