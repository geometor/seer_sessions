"""
The transformation rule involves identifying all pixels of color 2 (red) and color 6 (magenta) within the input grid.  Every instance of color 2 is changed to color 6, and every instance of color 6 is changed to color 2.  All other colors remain unchanged. The dimensions of the grid stay consistent.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Swap color 2 (red) with color 6 (magenta).
    output_grid[input_grid == 2] = 6
    # Swap color 6 (magenta) with color 2 (red).
    output_grid[input_grid == 6] = 2

    return output_grid