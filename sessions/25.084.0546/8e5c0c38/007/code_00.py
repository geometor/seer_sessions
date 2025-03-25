"""
Iterate through the non-background colored objects in the input grid.
For each object, remove the absolute leftmost pixel of that object.
"""

import numpy as np

def get_objects(grid):
    # Find all unique colors in the grid, excluding 0 (background)
    unique_colors = np.unique(grid)
    unique_colors = unique_colors[unique_colors != 0]
    
    objects = {}
    for color in unique_colors:
        # Create a mask for the current color
        mask = (grid == color)
        
        # Find the coordinates of all pixels of the current color
        coords = np.array(np.where(mask)).T
        
        # Store the color and coordinates as an object
        objects[color] = coords
    
    return objects

def get_leftmost_pixel(coords):
    # returns the leftmost pixel coordinates of an object
    # coords is a numpy array of (row, col) pairs

    min_col_index = np.argmin(coords[:, 1])
    return coords[min_col_index]

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()

    # Get objects from the input grid
    objects = get_objects(input_grid)

    # Iterate through each object
    for color, coords in objects.items():
      # Find the absolute leftmost pixel of the object.
      leftmost_pixel = get_leftmost_pixel(coords)

      # Remove the leftmost pixel
      output_grid[leftmost_pixel[0], leftmost_pixel[1]] = 0

    return output_grid