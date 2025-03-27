"""
The function takes an input grid of digits and returns an output grid of the same dimensions.
The output grid is filled entirely with the digit that appears in the last position of the last row of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid.
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Find the target digit (last digit in the last row).
    target_digit = input_grid[-1][-1]

    # Create an output grid with the same dimensions, filled with the target digit.
    output_grid = np.full((rows, cols), target_digit)

    return output_grid