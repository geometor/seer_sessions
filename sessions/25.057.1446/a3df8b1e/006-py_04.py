"""
Invert Colors: For every pixel in the input grid, swap 0s (white) and 1s (blue). Maintain the original grid dimensions.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions and data type as input grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate over each pixel of the input grid
    for i in range(rows):
        for j in range(cols):
            # Invert colors: If 0 (white), change to 1 (blue); if 1 (blue), change to 0 (white).
            output_grid[i, j] = 1 if input_grid[i, j] == 0 else 0

    return output_grid