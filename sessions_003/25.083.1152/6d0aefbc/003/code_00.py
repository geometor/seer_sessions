"""
The transformation rule takes a 3x3 input grid and produces a 3x6 output grid.
It duplicates each column of the input grid and places it in reverse order at the end of the output grid.
The original columns of the input grid are copied to the beginning of the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid (3x3) into an output grid (3x6) by
    copying the input grid and appending a mirrored version of the input grid's columns.
    """
    # Initialize the output grid with zeros, ensuring it's 3x6
    output_grid = np.zeros((3, 6), dtype=int)

    # Copy the original input grid to the first three columns of the output grid
    output_grid[:, 0:3] = input_grid
    
    # Copy each column of the input, and place into the output
    output_grid[:, 3] = input_grid[:, 2]
    output_grid[:, 4] = input_grid[:, 1]
    output_grid[:, 5] = input_grid[:, 0]

    return output_grid