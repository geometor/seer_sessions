"""
The transformation rule is a 180-degree rotation of the grid. The L-Shaped object made out of marron (9) pixels is being rotated.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Rotate the grid by 180 degrees.
    output_grid = np.rot90(output_grid, 2)

    return output_grid