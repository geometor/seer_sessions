"""
The transformation involves shifting cell values along the main diagonal down by one, wrapping around the grid boundaries. All other cells remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through columns
    for i in range(rows):
        # move the value
        output_grid[(i + 1) % rows, (i + 1) % cols] = input_grid[i,i]

    return output_grid