"""
The transformation inverts the first column of the input and then creates a second column in the output that alternates opposite colors with the first column.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # change output pixels 
    # First column inversion
    for i in range(rows):
        output_grid[i, 0] = 1 if input_grid[i, 0] == 0 else 0

    # Second column complementing
    for i in range(rows):
        output_grid[i, 1] = 1 if output_grid[i, 0] == 0 else 0

    return output_grid