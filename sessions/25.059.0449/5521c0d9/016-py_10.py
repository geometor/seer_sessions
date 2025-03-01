"""
Shift colored objects (blue vertical line, yellow rectangle, red horizontal line) upwards by a specific number of rows.
The blue line shifts up by 4 rows, the yellow rectangle by 2 rows, and the red line by 1 row.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of pixels of the specified color.
    coords = np.argwhere(grid == color)
    return coords

def shift_object_up(grid, coords, shift_amount):
    # Create a copy of the grid to modify.
    new_grid = np.copy(grid)

    # Remove the original object
    for r, c in coords:
        new_grid[r, c] = 0

    # Add the object back at the shifted position
    for r, c in coords:
        new_r = r - shift_amount
        if 0 <= new_r < new_grid.shape[0]: #keep within bounds
            new_grid[new_r, c] = grid[r,c]
    return new_grid
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find and shift the blue object.
    blue_coords = find_object(output_grid, 1)
    if len(blue_coords)>0:
      output_grid = shift_object_up(output_grid, blue_coords, 4)

    # Find and shift the yellow object.
    yellow_coords = find_object(output_grid, 4)
    if len(yellow_coords) > 0:
        output_grid = shift_object_up(output_grid, yellow_coords, 2)

    # Find and shift the red object
    red_coords = find_object(output_grid,2)
    if len(red_coords) > 0:
      output_grid = shift_object_up(output_grid, red_coords, 1)
    
    return output_grid