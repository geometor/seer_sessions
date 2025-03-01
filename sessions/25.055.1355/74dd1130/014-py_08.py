"""
The transformation involves a single swap of two adjacent cell values. Specifically, the value of the top-left cell (0, 0) and the value of the cell immediately to its right (0, 1) are exchanged. All the other values in the grid are un-changed.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # swap the values of cell (0, 0) and (0, 1)
    temp = output_grid[0, 0]
    output_grid[0, 0] = output_grid[0, 1]
    output_grid[0, 1] = temp

    return output_grid