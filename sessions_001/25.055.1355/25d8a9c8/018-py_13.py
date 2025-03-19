"""
The transformation rule is a color substitution applied to each pixel in the input grid. The output grid maintains the same dimensions as the input grid (3x3). The color mapping is as follows:

1.  If a pixel is Red (2) or White (0), it becomes White (0) in the output.
2.  If a pixel is Yellow (4) or Maroon (9), it becomes Gray (5) in the output.
3.  Other colors remain the same
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2 or input_grid[r,c] == 0:
                output_grid[r, c] = 0
            elif input_grid[r, c] == 4 or input_grid[r, c] == 9:
                output_grid[r, c] = 5
            else:
                output_grid[r,c] = input_grid[r,c] # in case there are colors not specified in color map

    return output_grid