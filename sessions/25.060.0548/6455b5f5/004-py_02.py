"""
1.  **Identify the Red Shape:** Locate the connected component of red (2) pixels.
2.  **Highlight:** Add an azure (8) pixel in the top-left corner of the grid, if there is a red pixel in that position.
3.  **Highlight:** Find the bottom-right most pixel that has value of 2 (red), add an azure pixel (8) to the right adjacent to that.
4.  **Fill:** starting from bottom-left corner of the grid, paint blue color (1) until the complete grid width.
5.  **Fill:** Paint all rows from the bottom until the bottom-most of red color is painted. Paint with blue, until the red shape stops the paint.
"""

import numpy as np

def find_red_shape(grid):
    """Finds the coordinates of all red pixels."""
    return np.where(grid == 2)

def highlight_top_left(grid, red_pixels):
    """Adds an azure pixel at the top-left corner if red exists."""
    if grid[0, 0] == 2:
        grid[0, 0] = 8
    return grid

def highlight_bottom_right(grid, red_pixels):
    """Adds an azure pixel to the right of the bottom-rightmost red pixel."""
    red_y, red_x = red_pixels
    if len(red_x) > 0:  # Check if any red pixels were found
       bottom_right_index = np.argmax(red_x)
       bottom_right_y = red_y[bottom_right_index]
       bottom_right_x = red_x[bottom_right_index]

       if bottom_right_x + 1 < grid.shape[1]:
           grid[bottom_right_y, bottom_right_x+1] = 8

    return grid
    

def fill_bottom(grid, red_pixels):
    """Fills the bottom area below the red shape with blue."""
    red_y, _ = red_pixels
    if (len(red_y) > 0):
        min_red_y = np.max(red_y)  #bottom-most y of red pixels
    else:
        min_red_y = 0

    for y in range(grid.shape[0] -1, min_red_y, -1):
      for x in range(0, grid.shape[1]):
        grid[y,x] = 1 #blue

    return grid


def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = input_grid.copy()

    # Find the red shape
    red_pixels = find_red_shape(output_grid)

    # Highlight corners
    output_grid = highlight_top_left(output_grid, red_pixels)
    output_grid = highlight_bottom_right(output_grid, red_pixels)
  
    #fill bottom
    output_grid = fill_bottom(output_grid, red_pixels)

    return output_grid