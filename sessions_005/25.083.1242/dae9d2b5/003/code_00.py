"""
Iterate through each pixel of the input grid. If a pixel's color is green (3) or yellow (4) AND its column index is less than half the width of the input grid (integer division), then the corresponding pixel in the output grid is magenta (6). Otherwise, if the input pixel's column is within the output's column range, keep the original color. Input pixels outside the output column range are ignored.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to serve as a basis for the output
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    output_cols = cols // 2

    #resize the output
    output_grid = output_grid[:, :output_cols]

    # Iterate through each cell within the bounds of the *output* grid
    for i in range(rows):
        for j in range(output_cols):
            # Conditional color change: 3 or 4 becomes 6, but ONLY within the output column range.
            if (input_grid[i, j] == 3 or input_grid[i, j] == 4):
                output_grid[i, j] = 6

    return output_grid