"""
The transformation rule involves selectively changing colors in the input grid. Specifically:

1.  If a pixel's color is 6 (magenta), 9 (maroon), or 4 (yellow), it is changed to 5 (gray).
2.  If a pixel's color is 1 (blue), it remains unchanged.
3.  Pixels of any other color are also meant to remain the same. (Although the provided examples do not *explicitly* show other colors, the instruction was to leave them unchanged).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # change output pixels based on the transformation rules
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 6:  # magenta
                output_grid[i, j] = 5  # gray
            elif output_grid[i, j] == 9:  # maroon
                output_grid[i, j] = 5  # gray
            elif output_grid[i, j] == 4:  # yellow
                output_grid[i, j] = 5  # gray
            # Implicitly, all other colors remain unchanged.
            # The explicit check for color 1 is not necessary,
            # as the default behavior is to leave other colors untouched.

    return output_grid