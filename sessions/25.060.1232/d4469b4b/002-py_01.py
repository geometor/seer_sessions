"""
The transformation identifies the presence of non-zero colored pixels in the top-left 3x3 region of input, and creates a 3x3 representation of the same area, turning any color except white to gray, leaving white pixels as white.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a 3x3 numpy array filled with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the top-left 3x3 subgrid of the input
    for i in range(3):
        for j in range(3):
            # If the corresponding input pixel is not 0, set the output pixel to 5
            if input_grid[i][j] != 0:
                output_grid[i][j] = 5
            # Otherwise, the output pixel remains 0 (initialized value)
            

    return output_grid