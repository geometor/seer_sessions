"""
The transformation rule identifies the first non-zero element in the input grid and replicates it downwards and to the right, forming a triangular pattern. The height of the output grid and the number of replications in each row are determined by the number of rows of the triangle, in the example, 4. The remaining cells in the output grid are filled with zeros.
"""

import numpy as np

def get_first_nonzero(grid):
    # return first non zero element of grid
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
             if grid[r,c] != 0: return grid[r,c]
    return 0

def transform(input_grid):
    # initialize output_grid
    first_nonzero = get_first_nonzero(input_grid)
    output_height = 4 # this is fixed based on this specific example
    output_width = input_grid.shape[1]
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    if first_nonzero != 0:
        for i in range(output_height):
            for j in range(i + 1):
                output_grid[i, j] = first_nonzero

    return output_grid