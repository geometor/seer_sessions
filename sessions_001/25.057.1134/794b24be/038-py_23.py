"""
1. Examine the top row of the input grid.
2. Create output, if the corresponding input pixel is blue(1), set output pixel to red(2); if the corresponding input pixel is white(0), output pixel to red(2)
3. The remaining rows in the output are all white.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as the input, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Iterate through the top row of the input grid.
    for i in range(input_grid.shape[1]):
        # if the input pixel is blue (1), change output to red (2).
        # if the input pixel is white(0), change the corresponding output pixel to red(2).
        if input_grid[0, i] == 1 or input_grid[0,i] == 0:
          output_grid[0,i] = 2

    return output_grid