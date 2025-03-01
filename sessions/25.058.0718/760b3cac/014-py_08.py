"""
Mirrors the top azure (8) object horizontally in the first three rows, leaving other objects and the background unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous blocks of non-zero pixels (objects) in the grid.
    Returns a dictionary of objects, keyed by color, with their pixel coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by mirroring the top azure object horizontally.
    """
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.copy(grid)  # Initialize output grid as a copy of the input
    objects = find_objects(grid)

    # Find and mirror the top azure object
    if 8 in objects:
        azure_objects = objects[8]
        
        # Find top object
        top_azure_object = min(azure_objects, key=lambda obj: min(r for r, _ in obj))


        # Mirror the top object horizontally (first three rows).
        for r, c in top_azure_object:
          if r < 3:
            output_grid[r, grid.shape[1] - 1 - c] = 8

    return output_grid.tolist()