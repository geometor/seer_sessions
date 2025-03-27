"""
If there's a red pixel in the input grid, then replace the *entire* output grid row where the red pixel would be in the same column, and insert the predefined pattern. If a red pixel is in none of these positions, do not make a change.
"""

import numpy as np

def find_red_pixel(grid):
    # Find the coordinates of the red pixel (value 2).
    rows, cols = np.where(grid == 2)
    if len(rows) > 0:
        return rows[0], cols[0]
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    output_grid[:] = 0

    # Find the red pixel in the input.
    red_pixel_coords = find_red_pixel(input_grid)

    # If a red pixel is found, apply the transformation.
    if red_pixel_coords:
        row, col = red_pixel_coords
        height = input_grid.shape[0]

        pattern = np.array([[3, 0, 6],
                            [0, 0, 0],
                            [8, 0, 7]])
        
        if row == 0 :
           output_grid[1,:] = [0,8,0,7,0]
        elif row == 1:
            if input_grid.shape[1] >= 3:
                output_grid[0, col-1:col+2] = pattern[0]
                output_grid[2, col-1:col+2] = pattern[2]
        elif row == 2:
            output_grid[1,:] = [0,8,0,7,0]

    return output_grid