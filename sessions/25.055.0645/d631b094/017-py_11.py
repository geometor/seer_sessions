"""
The output grid is always a 1x1 grid containing the first non-zero value found in the input grid, using a top-to-bottom, left-to-right scan. If no non-zero values are found, the output is a 1x1 grid containing 0.
"""

import numpy as np

def find_first_non_zero(grid):
    """Finds the first non-zero value in a grid."""
    for row in grid:
        for val in row:
            if val != 0:
                return val
    return 0  # Return 0 if no non-zero value is found

def transform(input_grid):
    """Transforms the input grid to the output grid."""
    # Find the first non-zero value in the input grid.
    first_non_zero_value = find_first_non_zero(input_grid)

    # Create a 1x1 output grid with the first non-zero value.
    output_grid = [[first_non_zero_value]]

    return output_grid