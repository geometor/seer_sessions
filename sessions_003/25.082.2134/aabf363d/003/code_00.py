"""
1.  **Identify the Signal Color:** Determine the color of the pixel located in the bottom-left corner of the input grid. This is the "signal color".
2.  **Iterate Through Grid:** Examine each pixel in the input grid, one by one.
3.  **Conditional Replacement:** For each pixel:
    *   If the pixel's color is *not* white (0) AND the pixel's color is *not* equal to the signal color, then change the pixel's color to the signal color.
    *   Otherwise if pixel is white, leave as-is
    *   Otherwise, it is the signal color, leave as-is
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # get dimensions of the input grid
    rows, cols = input_grid.shape

    # identify the "signal" color from the bottom-left corner
    signal_color = input_grid[rows - 1, 0]

    # iterate through each cell of the grid
    for i in range(rows):
        for j in range(cols):
            # check if the current pixel is not white and not the signal color
            if input_grid[i, j] != 0 and input_grid[i, j] != signal_color:
                # replace the pixel color with the signal color
                output_grid[i, j] = signal_color

    return output_grid