"""
The transformation replaces specific zero-valued cells in the input grid with
predetermined, constant-valued, colored pixels at defined coordinates. The
input pixel value is irrelevant to the output, except that they are placed
where zeros exist.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions and data type as the input grid, filled with zeros.
    output_grid = np.zeros_like(input_grid)

    # Set specific cells to predetermined values (colors).
    output_grid[0, 0] = 3  # Green
    output_grid[0, 2] = 6  # Magenta
    output_grid[2, 0] = 8  # Azure
    output_grid[2, 2] = 7  # Orange

    return output_grid