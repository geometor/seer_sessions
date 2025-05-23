"""
1.  **Identify** all yellow (4) pixels in the input grid.
2.  Locate any yellow pixels that are directly below the top-right most yellow pixel and is part of a cluster of at least one other yellow pixel, and is not boardered by yellow on both the left and right,
3. Or, locate any yellow pixel that is directly above another yellow that is part of a 3x2 yellow area.
4.  **Change** the color of the identified yellow pixels to orange (7).
5.  **Preserve** all other pixels (white and the remaining yellow) as they are in the input.
"""

import numpy as np

def get_yellow_pixels(grid):
    """
    Finds all yellow pixels in the grid
    """
    yellow_pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel == 4:
                yellow_pixels.append((row_idx, col_idx))
    return yellow_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    yellow_pixels = get_yellow_pixels(input_grid)

    # check each yellow if it meets conditions
    for row, col in yellow_pixels:
      try:
        # Condition 2: Directly below top-right of 3x2 and not bordered on both left/right by yellow
        if (input_grid[row-1, col-1] == 4 and
              input_grid[row-1,col] == 4 and
              input_grid[row-1, col+1] == 4 and
              input_grid[row, col+1] == 4 and
            not (input_grid[row,col-1] == 4 and input_grid[row, col+2] == 4)):
            output_grid[row, col] = 7

        # Condition 3, split into 3x2 and 2x3.
        if (input_grid[row+1,col] == 4 and
            input_grid[row+2,col] == 4 and
            input_grid[row+1, col-1] == 4 and
            input_grid[row+2,col-1] == 4 and
            input_grid[row+1, col+1] == 4 and
            input_grid[row+2,col+1] == 4):
            output_grid[row,col] = 7

      except IndexError:  # handles out-of-bounds errors
        pass

    return output_grid