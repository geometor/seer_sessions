"""
1.  Identify all red (2) pixels within the input grid.
2.  For each red pixel, check if there is a green (3) pixel directly to its right.
3. If a green pixel exists to the right, then the green pixel on the output must be changed to black (0).
4.  Copy any pixel from input that isn't changed in the prior steps.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid, checking for green pixels to the right of red pixels.
    for i in range(rows):
        for j in range(cols - 1):  # Check up to the second-to-last column
            if input_grid[i, j] == 2 and input_grid[i, j + 1] == 3:
                # Change the green pixel to black.
                output_grid[i, j + 1] = 0

    return output_grid