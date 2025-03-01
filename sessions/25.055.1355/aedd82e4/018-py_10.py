"""
The rightmost red pixel changes to blue.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    # change output pixels
    # Iterate through the grid from right to left, top to bottom
    for r in range(rows):
        for c in range(cols - 1, -1, -1):
            if output_grid[r, c] == 2:  # Check for red pixel
                output_grid[r, c] = 1  # Change to blue
                return output_grid  # Return immediately after the first change

    return output_grid