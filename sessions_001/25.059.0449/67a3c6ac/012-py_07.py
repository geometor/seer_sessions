"""
The transformation rule is a 180-degree rotation of the entire input grid. This is equivalent to performing both a horizontal and a vertical reflection.

1.  **Center Point:** Imagine a center point in the grid.  For grids with odd dimensions, this is the exact middle pixel.

2.  **Horizontal Reflection:** Each pixel's horizontal distance from the center is inverted. A pixel `x` units to the right of center in the input becomes `x` units to the left of center in the output, and vice versa.

3.  **Vertical Reflection:** Each pixel's vertical distance from the center is inverted. A pixel `y` units below the center in the input becomes `y` units above the center in the output, and vice versa.

4. **Combined Effect:** Steps 2 and 3 together achieve a 180-degree rotation around the grid's center.  The pixel at position (i, j) in the input grid moves to position (rows - 1 - i, cols - 1- j) in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # get dimensions of the input grid
    rows = len(input_grid)
    cols = len(input_grid[0])

    # iterate through each pixel of the input grid
    for i in range(rows):
        for j in range(cols):
            # calculate the mirrored indices for 180-degree rotation
            mirrored_i = rows - 1 - i
            mirrored_j = cols - 1 - j

            # assign pixel value from input to corresponding mirrored position in output
            output_grid[mirrored_i, mirrored_j] = input_grid[i, j]

    return output_grid