"""
1.  **Identify Target Pixel:** Examine the input grid. Locate the bottom-most, and then right-most red(2) pixel. If no red pixels exist go to 2.

2.  **Change Color:** If a red pixel is found, change it from red(2) to blue(1). If no red pixels exist, locate the last non-white(0) pixel reading down column 3 (index 2). From this location, moving down, add a blue(1) pixel below that, in the next available white(0) space.
"""

import numpy as np

def find_bottom_right_red(grid):
    """Finds the bottom-most, right-most red (2) pixel."""
    rows, cols = grid.shape
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] == 2:
                return (r, c)
    return None

def find_next_white_below(grid, col):
    """finds next white space in a column starting at row"""
    rows = grid.shape[0]

    last_non_white_row = -1
    for r in range(rows):
      if grid[r,col] != 0:
        last_non_white_row = r

    for r in range(last_non_white_row + 1, rows):
      if grid[r,col] == 0:
        return (r,col)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # find bottom-most, right-most red pixel
    red_pixel = find_bottom_right_red(output_grid)

    # change the color of identified pixel to blue
    if red_pixel:
        output_grid[red_pixel] = 1
    else:
      # find location for new blue
      insert_location = find_next_white_below(input_grid, 2)
      if insert_location:
        output_grid[insert_location] = 1

    return output_grid