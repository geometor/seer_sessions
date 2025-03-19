"""
1. Identify all red (value 2) pixels in the input grid.
2. Extract these red pixels, discarding all other colors.
3. Reshape the extracted red pixels into a 1x3 grid. In other words, create output to be a single row containing only the red pixels.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    red_pixels = []

    # find all red pixels
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] == 2:
                red_pixels.append(2)

    # reshape red pixels into a 1x3 grid
    output_grid = np.array(red_pixels).reshape(1, -1)
    if output_grid.shape[1] != 3:
      output_grid = np.resize(output_grid,(1,3))
      output_grid = np.array(output_grid,dtype=int)


    return output_grid.tolist()