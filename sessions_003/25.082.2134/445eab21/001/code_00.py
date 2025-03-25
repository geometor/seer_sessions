"""
Identifies the color of the largest object in the lower half of the input grid and creates a 2x2 output grid filled with that color.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all distinct objects (contiguous regions of non-zero pixels) in a grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, current_object):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append((grid[r, c], current_object))  # Store color and object pixels
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Find all objects in the grid
    objects = find_objects(np.array(input_grid))

    # Find the object with the lowest average row index (bottom-most object)
    lowest_object = None
    lowest_avg_row = -1

    for color, object_pixels in objects:
      avg_row = sum([r for r,c in object_pixels])/len(object_pixels)
      if lowest_avg_row == -1:
        lowest_avg_row = avg_row
        lowest_object = (color, object_pixels)
      elif avg_row > lowest_avg_row:
        lowest_avg_row = avg_row
        lowest_object = (color, object_pixels)


    # Extract the color of the lowest object
    output_color = lowest_object[0]

    # Create a 2x2 output grid filled with the extracted color
    output_grid = np.full((2, 2), output_color)

    return output_grid