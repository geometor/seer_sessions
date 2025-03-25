"""
Iterate through the non-background (non-zero) colored objects in the input grid.
For each object, remove the leftmost pixel of each row within that object.
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

def remove_leftmost_pixel_per_row(coords):
    # Create a dictionary to store row-wise coordinates
    row_coords = {}
    for x, y in coords:
        if x not in row_coords:
            row_coords[x] = []
        row_coords[x].append(y)

    # Identify and remove the leftmost pixel in each row
    pixels_to_remove = []
    for row, cols in row_coords.items():
        min_col = min(cols)
        pixels_to_remove.append((row, min_col))

    # remove marked pixels
    new_coords = []
    for x,y in coords:
      if (x,y) not in pixels_to_remove:
        new_coords.append((x,y))
    
    return np.array(new_coords)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()

    # Get objects from the input grid
    objects = get_objects(input_grid)

    # Iterate through each object
    for color, coords in objects.items():
      #remove left most pixel per row
      new_coords = remove_leftmost_pixel_per_row(coords)

      # remove old object
      for x, y in coords:
        output_grid[x, y] = 0
          
      # add modified object
      for x, y in new_coords:
          output_grid[x,y] = color

    return output_grid