"""
1.  **Locate:** Find the green pixel (value 3) within the input grid.
2.  **Move Down:** Move the green pixel down one row.
3.  **Bottom Row Wrap:** If the green pixel is on the last row before the move, move it to the first row (index 0) of the same column.
4.  **Preserve Positions:** Ensure all other pixels remain in place from input grid to output grid.
5.  **Output:** The output grid is identical to the input grid except for the green pixel's new position.
"""

import numpy as np

def find_pixel(grid, color_value):
    # find the coordinates of a pixel with a specified color value
    coords = np.where(grid == color_value)
    if len(coords[0]) > 0:  # Check if the pixel exists
       return (coords[0][0], coords[1][0])
    else: return None

def transform(input_grid):
    # initialize output_grid as a copy of input grid
    output_grid = np.copy(input_grid)
    grid_height = output_grid.shape[0]

    # find the green pixel
    green_pixel_coords = find_pixel(input_grid, 3)

    # Move the green pixel one row down with wrap-around if found
    if green_pixel_coords:
        r, c = green_pixel_coords
        output_grid[r, c] = 0  # remove from the original position
        new_r = (r + 1) % grid_height # calculate with wrap
        output_grid[new_r, c] = 3  # place in the new position
        
    return output_grid