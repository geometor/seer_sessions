"""
The transformation rule is: Find the color of the pixel in the bottom-left
corner of the input grid. Change all the pixels of a different, non-zero color
in the input grid to the color of the bottom-left pixel.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # get dimensions of the input grid
    rows, cols = input_grid.shape

    # identify the "signal" color from the bottom-left corner
    signal_color = input_grid[rows - 1, 0]

    # if signal color is white(0), return the original grid, since no change is needed.
    if signal_color == 0:
      return output_grid

    # iterate through each cell of the grid
    for i in range(rows):
        for j in range(cols):
            # check if the current pixel is not white and not the signal color
            if input_grid[i, j] != 0 and input_grid[i, j] != signal_color:
                # replace the pixel color with the signal color
                output_grid[i, j] = signal_color

    return output_grid