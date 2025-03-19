"""
The input grid is replicated and embedded multiple times within a larger 9x9 output grid. The original grid's content is placed at positions (0,0), (0,6), (3,3) and (6,0) of the output grid, and the rest of the grid is filled with zeros (white).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)

    # Embed the input grid at specified positions
    output_grid[0:3, 0:3] = input_grid
    output_grid[0:3, 6:9] = input_grid
    output_grid[3:6, 3:6] = input_grid
    output_grid[6:9, 0:3] = input_grid

    return output_grid