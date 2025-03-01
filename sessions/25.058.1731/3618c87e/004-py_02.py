"""
Swap the blue pixel with the center gray pixel on the bottom row.
"""

import numpy as np

def find_pixel_by_color(grid, color):
    """Finds the coordinates of the first pixel with the given color."""
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return (coords[0][0], coords[1][0])
    return None

def find_row_of_color(grid, color):
    """Finds the row index of the first row that is entirely of the given color"""
    for i, row in enumerate(grid):
      if np.all(row == color):
        return i
    return None
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find the blue pixel (1)
    blue_pixel_coords = find_pixel_by_color(input_grid, 1)

    # Find the bottom row of gray pixels (5)
    gray_row_index = find_row_of_color(input_grid,5)
   
    if blue_pixel_coords is None or gray_row_index is None:
        return output_grid #should not happen based on problem description, but good practice

    # Get original value where the 1 will go
    original_value = output_grid[gray_row_index, 2]

    # Move the blue pixel to the center of the bottom row
    output_grid[gray_row_index, 2] = 1

    # Move the value from target location to source location of blue pixel
    if blue_pixel_coords:
        output_grid[blue_pixel_coords] = original_value

    #return the modified output
    return output_grid