"""
The transformation rule is a simple color substitution. Each number in the input grid is replaced by a corresponding number in the output grid according to this direct mapping:

1.  Replace all occurrences of the number 5 with the number 1.
2.  Replace all occurrences of the number 8 with the number 9.
3.  Replace all occurrences of the number 6 with the number 2.

The shape and size of the grid do not change.
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