"""
1.  **Identify the Red Shape:** Locate all connected regions of red (2) pixels.

2.  **Highlight:** Find the right-most pixel of the red shape, regardless of its vertical position. Add an azure (8) pixel immediately to the right of this pixel. If adding the pixel would exceed the grid's boundaries, do not add it.

3.  **Fill:** Starting from the bottom row of the grid, fill every column in each row with blue (1).

4.  **Fill Stop:** Continue filling blue upwards until the row *above* the azure pixel. If no red pixels exists, there is also no azure pixel, and therefore no blue filling.
"""

import numpy as np

def find_red_pixels(grid):
    """Finds the coordinates of all red pixels."""
    return np.where(grid == 2)

def add_azure_highlight(grid, red_pixels):
    """Adds an azure pixel to the right of the rightmost red pixel."""
    red_y, red_x = red_pixels
    if len(red_x) > 0:
        rightmost_red_index = np.argmax(red_x)
        rightmost_red_y = red_y[rightmost_red_index]
        rightmost_red_x = red_x[rightmost_red_index]

        if rightmost_red_x + 1 < grid.shape[1]:
            grid[rightmost_red_y, rightmost_red_x + 1] = 8
    return grid

def fill_blue(grid, red_pixels):
    """Fills the bottom area with blue up to the row above the azure pixel."""
    red_y, red_x = red_pixels
    if len(red_x) > 0:
        rightmost_red_index = np.argmax(red_x)
        rightmost_red_y = red_y[rightmost_red_index]
        rightmost_red_x = red_x[rightmost_red_index]

        if rightmost_red_x + 1 < grid.shape[1]:
            stop_row = rightmost_red_y -1  #stop row is now one above the azure pixel.
        else:
          return grid
    else:
      return grid

    for y in range(grid.shape[0] - 1, stop_row , -1):  # Iterate upwards to the row *above* the azure
        for x in range(grid.shape[1]):
            grid[y, x] = 1
    return grid

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()

    # Find the red shape
    red_pixels = find_red_pixels(output_grid)

    # Highlight
    output_grid = add_azure_highlight(output_grid, red_pixels)

    # Fill
    output_grid = fill_blue(output_grid, red_pixels)

    return output_grid