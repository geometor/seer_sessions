"""
Removes interior shapes from the input grid, preserving only the outermost contiguous shapes of each color.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in a grid.
    Returns a list of objects, where each object is a set of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] == 0:
            return
        visited.add((row, col))
        current_object.add((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and (row, col) not in visited:
                current_object = set()
                dfs(row, col, current_object)
                objects.append((current_object, grid[row,col]))  # Store the object and its color
    return objects

def is_completely_enclosed(obj1, obj2):
    """
    Checks if obj1 is completely enclosed by obj2.

    Args:
      obj1: set of (row, col) tuples.
      obj2: set of (row, col) tuples.
    Returns:
      True if obj1 is completely enclosed by obj2, otherwise False.
    """
    if obj1 == obj2:
        return False

    min_r1, min_c1 = float('inf'), float('inf')
    max_r1, max_c1 = float('-inf'), float('-inf')
    for r, c in obj1:
        min_r1 = min(min_r1, r)
        max_r1 = max(max_r1, r)
        min_c1 = min(min_c1, c)
        max_c1 = max(max_c1, c)

    min_r2, min_c2 = float('inf'), float('inf')
    max_r2, max_c2 = float('-inf'), float('-inf')
    for r, c in obj2:
        min_r2 = min(min_r2, r)
        max_r2 = max(max_r2, r)
        min_c2 = min(min_c2, c)
        max_c2 = max(max_c2, c)


    # Check if obj1's bounding box is entirely within obj2's bounding box.
    if min_r2 <= min_r1 and max_r1 <= max_r2 and min_c2 <= min_c1 and max_c1 <= max_c2:
        # Check that no part of obj1 is on the boundary of obj2
        for r, c in obj1:
          if r == min_r2 or r == max_r2 or c == min_c2 or c == max_c2:
            #Check to see if the boundary pixel is part of the other object
            if (r,c) in obj2:
                return False
        return True
    return False

def transform(input_grid):
    """
    Transforms the input grid by removing interior shapes.
    """
    grid = np.array(input_grid)  # Convert to NumPy array
    objects = find_objects(grid)
    output_grid = np.zeros_like(grid)

    # Determine which objects to remove
    objects_to_remove = set()
    for i in range(len(objects)):
        for j in range(len(objects)):
            if is_completely_enclosed(objects[i][0], objects[j][0]):
                objects_to_remove.update(objects[i][0])

    # Copy non-removed pixels to output_grid
    for obj, color in objects:
        if not any(coord in objects_to_remove for coord in obj):
            for row, col in obj:
                output_grid[row, col] = color

    return output_grid.tolist()