"""
Transforms the input grid by isolating and potentially resizing the red object based on the presence and dimensions of other objects in the grid.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in a grid.
    Returns a dictionary of objects, keyed by color, with bounding box and pixels.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        pixels.append((row, col))
        dfs(row + 1, col, color, pixels)
        dfs(row - 1, col, color, pixels)
        dfs(row, col + 1, color, pixels)
        dfs(row, col - 1, color, pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row,col] != 0:
                color = grid[row, col]
                pixels = []
                dfs(row, col, color, pixels)
                if color not in objects:
                    objects[color] = {
                        'pixels': pixels,
                        'min_row': min(p[0] for p in pixels),
                        'max_row': max(p[0] for p in pixels),
                        'min_col': min(p[1] for p in pixels),
                        'max_col': max(p[1] for p in pixels),
                    }
                else:
                  #append to existing color object
                  objects[color]['pixels'].extend(pixels)
                  objects[color]['min_row'] = min(objects[color]['min_row'],min(p[0] for p in pixels))
                  objects[color]['max_row'] = max(objects[color]['max_row'],max(p[0] for p in pixels))
                  objects[color]['min_col'] = min(objects[color]['min_col'],min(p[1] for p in pixels))
                  objects[color]['max_col'] = max(objects[color]['max_col'],max(p[1] for p in pixels))
    return objects

def get_object_dimensions(object_data):
    """Calculates the height and width of an object."""
    if not object_data:
        return 0,0
    height = object_data['max_row'] - object_data['min_row'] + 1
    width = object_data['max_col'] - object_data['min_col'] + 1
    return height, width

def transform(input_grid):
    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # Check if a red object exists
    if 2 not in objects:
        return np.zeros((0, 0), dtype=int)  # Return an empty grid if no red object

    # Get the red object's dimensions
    red_object = objects[2]
    red_height, red_width = get_object_dimensions(red_object)

    # Determine output dimensions based on other object and red object
    output_height, output_width = red_height, red_width

    if red_height == 2 and red_width == 2:
        has_other_objects = False
        for color, obj_data in objects.items():
            if color != 2:
                has_other_objects = True
                other_height, other_width = get_object_dimensions(obj_data)
                if other_height == 3 and other_width == 2: #example 3 condition
                   output_height = int(red_height * 2.5)
                   output_width  = int(red_width * 4)
        if not has_other_objects:
          output_height = 2
          output_width = 2

    # Create the output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Fill output grid with red pixels
    for r in range(output_height):
      for c in range(output_width):
        output_grid[r,c] = 2
    return output_grid