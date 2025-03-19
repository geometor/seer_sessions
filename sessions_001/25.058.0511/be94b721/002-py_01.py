"""
Extracts and simplifies the red (value 2) object from the input grid, discarding all other colored objects, and returns a new grid containing only the reshaped, cropped minimal boundary of the red object.
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

def transform(input_grid):
    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # Check if a red object exists
    if 2 not in objects:
        return np.zeros((0, 0), dtype=int)  # Return an empty grid if no red object

    # Get the red object's bounding box
    red_object = objects[2]
    min_row, max_row = red_object['min_row'], red_object['max_row']
    min_col, max_col = red_object['min_col'], red_object['max_col']

    # Create a new grid containing only the red object
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)
    for row, col in red_object['pixels']:
        output_grid[row - min_row, col - min_col] = 2

    return output_grid