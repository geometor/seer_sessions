"""
Transforms an input grid based on color-specific rules, primarily focusing on
the interaction between vertically adjacent pixels and the influence of the second-to-last row.

1. **Initialization:** The output grid starts as a copy of the input grid.
2. **Gray (5) to Blue (1) on Last Row:** If a pixel in the second-to-last row is gray (5) and the pixel *directly above* it is *not* black (0), the corresponding pixel on the last row of the output grid becomes blue (1).
3. **Preservation:** All other pixels remain unchanged.
"""

import numpy as np

def get_vertically_adjacent_above(grid, row, col):
    """Returns the pixel directly above the given cell, or None if at the top."""
    if row > 0:
        return grid[row - 1, col]
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape
    last_row = rows - 1

    # iterate through the second-to-last row
    for c in range(cols):
        # check the second-to-last row for gray(5)
        if input_grid[last_row -1, c] == 5:
            # check if cell above is not black (0)
            above = get_vertically_adjacent_above(input_grid, last_row - 1, c)
            if above != 0 and above is not None:
                # change corresponding last row cell to blue (1)
                output_grid[last_row, c] = 1

    return output_grid