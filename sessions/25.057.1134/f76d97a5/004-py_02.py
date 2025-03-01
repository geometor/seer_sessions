"""
1. Iterate through every cell in the input grid.
2. If a cell's value is 5 (gray), change it to 0 (white).
3. If a cell's value is any other color, retain the original value.
4. The output grid has the same dimensions and cell positions as the input grid. Only the specified color change is made.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # change output pixels
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 5:
                output_grid[i, j] = 0

    return output_grid