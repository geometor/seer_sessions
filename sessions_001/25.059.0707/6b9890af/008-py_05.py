"""
The transformation extracts a region around the azure and red shapes in the input, creates a smaller 8x8 grid with a red border, and positions a transformed/resized versions of azure shapes within this new grid, keeping some relative positioning and filling with white color.
"""

import numpy as np

def find_objects(grid, color):
    # Find objects of a specific color in the grid.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return []
    return coords

def get_bounding_box(coords):
    # Calculate the bounding box of a set of coordinates.

    min_y, min_x = np.min(coords, axis=0)
    max_y, max_x = np.max(coords, axis=0)
    return min_y, min_x, max_y, max_x
  

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((8, 8), dtype=int)

    # Create red border
    output_grid[0, :] = 2
    output_grid[-1, :] = 2
    output_grid[:, 0] = 2
    output_grid[:, -1] = 2
    
    # Find azure objects
    azure_coords = find_objects(input_grid, 8)
    
    # if no azure objects, return current output
    if not azure_coords.any():
       return output_grid

    # Get azure bounding box.
    min_y, min_x, max_y, max_x = get_bounding_box(azure_coords)
    
    # Calculate center
    center_x = (min_x + max_x) // 2
    
    # Place azure rectangles in output.
    output_grid[1:3, center_x - min_x + 2: center_x-min_x + 4] = 8
    output_grid[4:6, center_x - min_x + 2: center_x-min_x + 4] = 8
    output_grid[2:4, 1:3] = 8
    output_grid[2:4, 5:7] = 8


    return output_grid