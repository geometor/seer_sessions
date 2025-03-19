"""
Change all blue (1) and azure (8) pixels to gray (5). Keep red (2) pixels the same.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # change output pixels based on color rules
            if output_grid[i, j] == 1 or output_grid[i, j] == 8:
                output_grid[i, j] = 5
            elif output_grid[i, j] == 2:
                output_grid[i, j] = 2  # Red remains unchanged (though redundant, it clarifies the logic)

    return output_grid