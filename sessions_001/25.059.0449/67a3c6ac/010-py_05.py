"""
The transformation rule is a "double reflection" or a 180-degree rotation.

1. **Horizontal Reflection:** For each pixel in the input grid, its corresponding pixel in the output grid is located at the horizontally mirrored position. Specifically, if a pixel is `x` positions away from the center column in the input, its corresponding pixel in the output is `x` positions away from the center column on the *opposite* side.

2. **Vertical Reflection:** Simultaneously, the same principle applies vertically. If a pixel is `y` positions away from the center row in the input, its output counterpart is `y` positions away from the center row on the *opposite* side.

3. Center point: Because the array has a odd number of rows and columns (7x7), the array will be reflected over the center point, (3,3).

In essence, each pixel's position is inverted relative to both the center column and the center row. This is equivalent to rotating the entire grid by 180 degrees around its center point.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)
    
    # get dimensions for looping and center point calculation
    rows = len(input_grid)
    cols = len(input_grid[0])

    # iterate through each pixel of the input grid
    for i in range(rows):
        for j in range(cols):
            # calculate mirrored indices
            mirrored_i = rows - 1 - i
            mirrored_j = cols - 1 - j

            # assign the value from input at (i, j) to the output at mirrord location
            output_grid[mirrored_i, mirrored_j] = input_grid[i, j]

    return output_grid