"""
Identifies the smallest object in the input grid, and copies it to an output grid of the same size.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all distinct objects in a grid.  An object is a contiguous set of
    pixels with same value.

    Returns a dictionary of objects, keyed by color,
    with each entry containing a list of (row, col) coordinates.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color, coords):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        coords.append((row, col))
        dfs(row + 1, col, color, coords)
        dfs(row - 1, col, color, coords)
        dfs(row, col + 1, color, coords)
        dfs(row, col - 1, color, coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                if color not in objects:
                    objects[color] = []
                coords = []
                dfs(row, col, color, coords)
                objects[color].append(coords)
    return objects

def find_smallest_object(objects):
    """
    Finds the smallest object among all colors.  If there are multiple objects
    of the same smallest size, select the one whose top-left corner is
    furthest to the top and then furthest to the left in the grid.
    """
    min_size = float('inf')
    target_object = None
    
    for color, obj_list in objects.items():
        for obj_coords in obj_list:
            size = len(obj_coords)
            if size < min_size:
                min_size = size
                target_object = obj_coords
            elif size == min_size:
                # Tie-breaker: Top-most, then left-most
                min_row_current = min(r for r, _ in target_object)
                min_col_current = min(c for _, c in target_object)
                min_row_new = min(r for r, _ in obj_coords)
                min_col_new = min(c for _, c in obj_coords)

                if min_row_new < min_row_current or (min_row_new == min_row_current and min_col_new < min_col_current):
                    target_object = obj_coords
    return target_object

def get_object_bounds(coords):
    """
    get the min and max row and col to determine bounding box
    """
    min_row = min(r for r, _ in coords)
    max_row = max(r for r, _ in coords)
    min_col = min(c for _, c in coords)
    max_col = max(c for _, c in coords)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find all objects in the input grid.
    objects = find_objects(input_grid)

    # Find the smallest object.
    target_object = find_smallest_object(objects)

    if target_object:
      # Determine the bounding box of the target object.
      min_row, max_row, min_col, max_col = get_object_bounds(target_object)

      # Create an output grid of the same size as the bounding box, filled with white (0).
      output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

      # Copy the object to the output grid, maintaining original positions
      for r, c in target_object:
        output_grid[r - min_row, c - min_col] = input_grid[r, c]

    else:
      output_grid = np.zeros_like(input_grid) # if no objects return empty grid

    return output_grid