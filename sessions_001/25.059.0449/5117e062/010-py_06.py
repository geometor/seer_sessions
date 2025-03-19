"""
1. Identify the green object (color 3): Locate the contiguous block of pixels with the value '3' in the input grid.
2. Define the object bounding box:  Determine a minimal rectangle that contains only the object with color 3.
3. Extract: Create the output using the bounding box.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels with the specified color.
    coords = np.argwhere(grid == color)
    return coords

def bounding_box(coords):
    # calculate the bounding box
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the green object (color 3).
    green_coords = find_object(input_grid, 3)

    # Handle the case where there's no green object.
    if len(green_coords) == 0:
      return np.zeros((3,3), dtype=int)
      
    # Get the bounding box of the green object.
    min_row, max_row, min_col, max_col = bounding_box(green_coords)

    # extract the object
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid