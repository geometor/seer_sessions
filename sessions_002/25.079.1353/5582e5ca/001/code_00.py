"""
The output grid is filled entirely with the color of the bottom-middle cell of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Find the bottom-middle cell's value.  For this to work, we must
    # assume the grid will always have an odd number of columns
    bottom_middle_value = input_grid[rows - 1][cols // 2]

    # Create an output grid of the same size, filled with the selected value.
    output_grid = np.full((rows, cols), bottom_middle_value)

    return output_grid