"""
The transformation involves changing a single red (2) pixel to blue (1). The red pixel to be changed is always located at the fourth column of the input grid. The row of the pixel changes, but it is always in the fourth column (index 3).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # find the red pixel in the fourth column
    red_pixels = np.argwhere(input_grid[:, 3] == 2)
    
    if len(red_pixels) > 0:
      # get row index, and change that pixel to blue.
      row_index = red_pixels[0,0]
      output_grid[row_index, 3] = 1

    return output_grid