"""
1.  Examine the input grid: Count the number of red pixels (pixels with a value of 2).
2.  Conditional Transformation:
    *   If red pixels are present: Extract all red pixels from the input grid. Arrange these extracted red pixels into a single row to form the output grid. The order of extraction should match a row major traversal (left to right, top to bottom).
    *   If no red pixels are present: The output grid is identical to the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize input_grid as numpy array
    input_grid = np.array(input_grid)
    red_pixels = []

    # find all red pixels using row major traversal
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] == 2:
                red_pixels.append(2)

    # if red pixels exist, create output grid, otherwise, the output is the input
    if len(red_pixels) > 0:
      output_grid = np.array(red_pixels).reshape(1, -1)
    else:
      output_grid = input_grid

    return output_grid.tolist()