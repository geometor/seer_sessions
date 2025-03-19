"""
1.  Identify Red and Yellow Pixels: Locate all pixels with the color red (value 2) and yellow (value 4) in the input grid.
2.  Swap Colors:
    *   Change the color of all identified red pixels to yellow (value 4).
    *   Change the color of all identified yellow pixels to red (value 2).
3.  Preserve Other Colors: Leave all other pixels in the grid unchanged.
4.  Output: The resulting grid is the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all red and yellow pixels
    red_pixels = np.argwhere(input_grid == 2)
    yellow_pixels = np.argwhere(input_grid == 4)

    # Change all red pixels to yellow
    for r, c in red_pixels:
        output_grid[r, c] = 4

    # Change all yellow pixels to red
    for r, c in yellow_pixels:
        output_grid[r, c] = 2

    return output_grid