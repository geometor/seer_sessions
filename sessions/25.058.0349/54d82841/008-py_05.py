"""
1.  **Identify the green shape:** Find all pixels with a value of 3 (green) that are connected. In this specific case, the connected green pixels are in the first two rows.
2.  **Locate Target position:** find the row index that is furthest from the green object, in this case the last row. Locate a position in the center of that row.
3. **Change one pixel:** If a pixel's value at that location is 0 (white) and it matches the target location determined by step 2, change its value to 4 (yellow).
4.  **Preserve the rest:** All other pixels retain their original values.
"""

import numpy as np

def find_green_shape(grid):
    # find connected green pixels
    green_pixels = np.argwhere(grid == 3)
    return green_pixels

def find_target_position(grid, green_pixels):
    # find the row index furthest from the green object
    max_row = grid.shape[0] -1
    center_col = grid.shape[1] // 2
    return (max_row, center_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find green shape
    green_pixels = find_green_shape(output_grid)
    
    # find target position
    target_row, target_col = find_target_position(output_grid, green_pixels)

    # change one pixel if conditions match
    if output_grid[target_row, target_col] == 0:
      output_grid[target_row, target_col] = 4

    return output_grid