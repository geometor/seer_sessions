"""
The transformation rule involves changing specific colors in the input grid to color 5, while leaving other colors unchanged. The colors 1, 6, 9, and 4 are the focus of the transformation.
1 remains the same, while 6, 9, and 4 are all changed to 5. Other colors are unaffected.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # change output pixels based on the transformation rules
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 6:
                output_grid[i, j] = 5
            elif output_grid[i, j] == 9:
                output_grid[i, j] = 5
            elif output_grid[i, j] == 4:
                output_grid[i, j] = 5

    return output_grid