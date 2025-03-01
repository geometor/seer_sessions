"""
The transformation rule is a cyclical color substitution: 1 -> 2, 2 -> 3, and 3 -> 1. Other colors remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a cyclical color substitution to the input grid.
    """
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel in the grid
    for row_index, row in enumerate(output_grid):
        for col_index, pixel_value in enumerate(row):
            # Apply the color substitution rules
            if pixel_value == 1:
                output_grid[row_index, col_index] = 2
            elif pixel_value == 2:
                output_grid[row_index, col_index] = 3
            elif pixel_value == 3:
                output_grid[row_index, col_index] = 1

    return output_grid