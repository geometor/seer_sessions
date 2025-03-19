"""
The program takes a grid as input. The output grid has the same dimensions (height and width) as the input grid. Every pixel in the output grid is black (0), regardless of the input pixel's value.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as input_grid, filled with 0s
    output_grid = np.zeros_like(input_grid)

    # No need for an explicit loop, as the entire array is already filled with 0s

    return output_grid