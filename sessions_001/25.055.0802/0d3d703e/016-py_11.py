"""
The transformation rule is a color substitution. The input grid's dimensions remain unchanged. The following substitutions are applied:

1.  Gray (5) pixels are replaced with Blue (1) pixels.
2.  Azure (8) pixels are replaced with Maroon (9) pixels.
3.  Magenta (6) pixels are replaced with Red (2) pixels.
4. All other colors remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Define the color mapping
    color_map = {
        5: 1,
        8: 9,
        6: 2
    }

    # Iterate through the grid and apply the color mapping
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] in color_map:
                output_grid[i, j] = color_map[output_grid[i, j]]

    return output_grid