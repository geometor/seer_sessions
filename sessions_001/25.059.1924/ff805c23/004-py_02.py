"""
Extract a 5x5 subgrid from the upper-left corner of the input grid and keep only pixels of color 0 and 3.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a 5x5 array filled with 0s (white)
    output_grid = np.zeros((5, 5), dtype=int)

    # Iterate through the 5x5 region in the upper-left corner of the input
    for i in range(5):
        for j in range(5):
            # Check if the pixel's color in the input grid is 0 or 3
            if input_grid[i][j] == 0 or input_grid[i][j] == 3:
                # If so, copy the pixel to the output grid
                output_grid[i][j] = input_grid[i][j]
            else:
                # if not, pixel becomes 0
                output_grid[i][j] = 0

    return output_grid