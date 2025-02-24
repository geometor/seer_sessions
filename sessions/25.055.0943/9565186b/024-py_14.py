"""
The transformation rule is as follows:

1.  Examine each pixel in the input grid.
2.  If the pixel is blue (1), change it to grey (5).
3.  If the pixel is yellow (4), keep it unchanged.
4.  If the pixel is green (3), keep it unchanged.
5. If the pixel is Grey(5), keep it unchanged.
6.  All other pixels (if any) should also remain unchanged. Essentially preserve Yellow(4), green (3) and Grey(5).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Change any 1(blue) pixel to 5 (grey).
            if output_grid[i, j] == 1:
                output_grid[i, j] = 5
            # Keep all pixels that are color 4 (yellow) or 3(green) or 5(grey)
            # unchanged. (Implicitly handled by copying the input grid initially)

    return output_grid