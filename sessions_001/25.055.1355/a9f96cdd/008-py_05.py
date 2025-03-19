"""
1.  **Find the Red Pixel:** Scan the input grid to locate the single red pixel (value '2'). Note its row and column coordinates.
2.  **Calculate New Position:** Determine the new position for a non-white pixel by subtracting 1 from the red pixel's row coordinate and 1 from its column coordinate.
3. **Create output grid:** create a grid the same size as the input grid.
4.  **Place the Green Pixel:** In the output grid, set the pixel value at the new position (calculated in step 2) to '3' (green).
5. **Clear initial position:** In the output grid set the value of the input grid's red pixel coordinates to '0'
6. **Fill Background:** In the output grid, all other grid positions should have a value of '0' (white).
"""

import numpy as np

def find_pixel(grid, color_value):
    # Find the coordinates of a pixel with a specific color value.
    rows, cols = np.where(grid == color_value)
    if len(rows) > 0:
        return rows[0], cols[0]  # Return the first occurrence
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the red pixel (value 2)
    red_pixel_pos = find_pixel(input_grid, 2)

    if red_pixel_pos:
        # Calculate the new position
        new_row = red_pixel_pos[0] - 1
        new_col = red_pixel_pos[1] - 1
      
        # Check for boundaries - important since it could try to place a pixel off the edge
        if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:

          # Place the green pixel (value 3)
          output_grid[new_row, new_col] = 3

        # clear the initial position
        output_grid[red_pixel_pos[0], red_pixel_pos[1]] = 0


    return output_grid