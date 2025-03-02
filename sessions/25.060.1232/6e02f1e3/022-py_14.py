"""
The transformation rule recolors the input grid based on the row index. The first row becomes gray, and all other rows become white.
"""

import numpy as np

def transform(input_grid):
    # Create an output grid with the same dimensions as the input, initialized to white (0).
    output_grid = np.zeros_like(input_grid)

    # Set the top row to gray (5).
    output_grid[0, :] = 5

    # The other rows are already white (0) due to initialization, so no further action needed.

    return output_grid