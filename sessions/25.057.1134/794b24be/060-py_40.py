"""
Colors the top-most row of the input grid red, and sets all other pixels to white.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid, but all white.
    output_grid = np.zeros_like(input_grid)

    # Color the top-most row (index 0) red.
    output_grid[0, :] = 2

    return output_grid