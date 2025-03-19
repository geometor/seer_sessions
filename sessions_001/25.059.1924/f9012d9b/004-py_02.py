"""
The transformation rule extracts the top-right 2x2 subgrid from the input grid, 
ignoring any white pixels, and uses this as the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the top-right 2x2 subgrid from the input grid.
    """
    # Get the dimensions of the input grid
    rows, cols = input_grid.shape

    # Extract the top-right 2x2 subgrid
    output_grid = input_grid[0:2, cols-2:cols]

    return output_grid