"""
Find the green pixel. Move the green pixel up by one row. Keep every other pixel the same.
"""

import numpy as np

def find_pixel_by_color(grid, color):
    # Find the coordinates of a pixel of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size > 0:
        return coords[0]  # Return the first occurrence
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the green (3) pixel
    green_pixel_coords = find_pixel_by_color(input_grid, 3)

    # Move the green pixel up by one row if it exists
    if green_pixel_coords is not None:
        new_row = green_pixel_coords[0] - 1
        old_row = green_pixel_coords[0]
        col = green_pixel_coords[1]
        
        #only if the move doesn't take it outside the grid
        if new_row >= 0:
            output_grid[old_row, col] = 0  # Set the old position to white (0)
            output_grid[new_row, col] = 3    # Set the new position to green (3)

    return output_grid