"""
The transformation rule appears to be conditional based on input shape:

1. **Identity Rule** If the height of input grid is greater than or equal to the width of the input grid, the output is not scaled, i.e., it is identical to the input.

2. **Replication Rule**: If the width of the input grid is greater than the height, double the input grid in both dimensions (horizontally and vertically). Each pixel in the input grid becomes a 2x2 block of the same color in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows, cols = input_grid.shape

    if rows >= cols:
        # Identity Rule
        output_grid = input_grid.copy()
    else:
        # Replication Rule
        output_grid = np.zeros((rows * 2, cols * 2), dtype=int)
        # change output pixels 
        for i in range(rows):
            for j in range(cols):
                color = input_grid[i, j]
                output_grid[2*i:2*i+2, 2*j:2*j+2] = color

    return output_grid