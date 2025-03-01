"""
Identify all contiguous regions (shapes) of grey (5) pixels.
For the top-most grey shape, fill its interior pixels (all non-outline grey pixels) with azure (8).
For the bottom-most grey shape, fill its interior pixels (all non-outline grey pixels) with orange (7).
Leave all white (0) background pixels unchanged.
"""

import numpy as np

def find_objects(grid, color):
    # Find all objects of a specific color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_object):
        if not is_valid(x, y) or visited[x, y] or grid[x, y] != color:
            return
        visited[x, y] = True
        current_object.append((x, y))
        dfs(x + 1, y, current_object)
        dfs(x - 1, y, current_object)
        dfs(x, y + 1, current_object)
        dfs(x, y - 1, current_object)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == color and not visited[x, y]:
                current_object = []
                dfs(x, y, current_object)
                objects.append(current_object)
    return objects

def get_outline(obj):
    # using a simplified outline definition.
    outline = set()
    for x, y in obj:
        is_outline = False
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < 30 and 0 <= ny < 30 and (nx, ny) in obj): # Simplified border check
                is_outline = True
                break
        if is_outline:
            outline.add((x,y))
    return outline

def fill_interior(grid, obj, color):
    # Fill interior pixels of an object with color
    outline = get_outline(obj)
    for x, y in obj:
        if (x,y) not in outline:
            grid[x, y] = color
            

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)

    # Find grey objects
    grey_objects = find_objects(input_grid, 5)
    
    # Sort objects by top-most position (smallest x value)
    grey_objects.sort(key=lambda obj: min(x for x, _ in obj))

    # Fill the interior of the top-most shape with azure (8)
    if len(grey_objects) >= 1:
      fill_interior(output_grid, grey_objects[0], 8)

    # Fill the interior of the second top-most shape, which is the bottom, with orange (7)
    if len(grey_objects) >= 2:
      fill_interior(output_grid, grey_objects[1], 7)

    return output_grid