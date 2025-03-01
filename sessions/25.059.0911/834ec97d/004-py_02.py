"""
1.  Identify the single red pixel (value 2) in the input grid.
2.  Record the original position of the red pixel.
3.  Move the red pixel down by one row.
4.  Create a new yellow pixel (value 4) at the original position of the red pixel.
5.  All the other cells maintain the background color of 0.
"""

import numpy as np

def find_pixel_by_color(grid, color_value):
    # Find the coordinates of a pixel with the specified color value.
    coords = np.where(grid == color_value)
    if len(coords[0]) > 0:
        return [coords[0][0], coords[1][0]]  # return first occurance
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find the red pixel (value 2).
    red_pixel_pos = find_pixel_by_color(input_grid, 2)

    # Move the red pixel down by one row.
    if red_pixel_pos:
        new_red_pos = [red_pixel_pos[0] + 1, red_pixel_pos[1]]
        
        #check bounds
        if(new_red_pos[0]>=0 and new_red_pos[0]<output_grid.shape[0]):
          output_grid[red_pixel_pos[0], red_pixel_pos[1]] = 0  # Remove from original position
          output_grid[new_red_pos[0], new_red_pos[1]] = 2    # Place in new position

        # Create a yellow pixel (value 4) at the red pixel's original position.
          output_grid[red_pixel_pos[0], red_pixel_pos[1]] = 4

    return output_grid