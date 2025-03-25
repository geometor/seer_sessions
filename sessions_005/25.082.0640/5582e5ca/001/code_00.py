"""
The transformation rule is to replace the entire input grid with a new grid where every cell has the value of the last number of the first input row.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid.
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Identify the target value (last number of the first row).
    target_value = input_grid[0][-1]

    # Construct output grid and populate.
    output_grid = np.full((rows, cols), target_value)

    return output_grid