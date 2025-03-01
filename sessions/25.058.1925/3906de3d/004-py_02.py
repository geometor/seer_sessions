"""
The transformation identifies a blue (1) rectangle and a red (2) vertical line.
The blue rectangle remains unchanged. The red line moves upwards to be
positioned directly below the blue rectangle, maintaining its original column.
The background (0) remains.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Handle case where color is not found
    return coords

def find_rectangle(grid, color):
    # assumes rectangular object - returns top-left and bottom-right corners
    coords = find_object(grid,color)
    if coords is None:
      return None
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # initialize output_grid as copy of input grid
    output_grid = np.copy(input_grid)

    # Find the blue rectangle.
    blue_coords = find_rectangle(input_grid, 1)
    if blue_coords is None: #handle no blue
      return output_grid

    # Find the red object.
    red_coords = find_object(input_grid, 2)
    if red_coords is None: #handle no red
      return output_grid

    # determine blue lowest extent
    blue_bottom = blue_coords[1][0]

    # Get the column of the red object.
    red_col = red_coords[0][1]

    # calculate how tall the red object is
    red_height = len(red_coords)

    # Erase the original red pixels from output
    for r, c in red_coords:
        output_grid[r, c] = 0

    # Move the red object upwards, just below the blue.
    new_red_top = blue_bottom
    for i in range(red_height):
      output_grid[new_red_top + i, red_col] = 2
    

    return output_grid