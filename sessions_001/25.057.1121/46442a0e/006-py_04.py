"""
The input 2x2 grid is replicated four times to create the output 4x4 grid. The input grid is duplicated horizontally and vertically to fill the output grid. This is a simple tiling operation.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.tile(input_grid, (2, 2))

    return output_grid