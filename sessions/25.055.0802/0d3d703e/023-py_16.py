"""
The transformation rule is a simple color substitution. The input grid is transformed into the output grid by replacing each pixel's color with a different, predetermined color. Specifically, azure (9) is replaced with blue (8), yellow (4) is replaced with green (3), and red (2) is replaced with magenta (6). All other colors remain unchanged (although no other colors appear in the input). The dimensions of the grid stay the same.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # define the color mapping
    color_map = {
        9: 8,
        4: 3,
        2: 6
    }

    # iterate through each pixel in the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # apply color mapping
            if output_grid[i, j] in color_map:
                output_grid[i, j] = color_map[output_grid[i, j]]

    return output_grid