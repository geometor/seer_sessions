"""
The transformation involves finding all of instances of the color 'yellow' and then to reproduce input as an output grid with every value is equal to 'yellow'.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as the input_grid
    output_grid = np.full(input_grid.shape, 4)

    return output_grid