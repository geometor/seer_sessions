"""
The transformation rule appears to be:  Gray (5) pixels in the input grid are changed to Green (3) in the output grid, while all other pixels remain the same.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.  This automatically
    # handles pixels that don't change.
    output_grid = np.copy(input_grid)

    # Iterate through the grid, changing gray pixels to green.
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                output_grid[r, c] = 3

    return output_grid