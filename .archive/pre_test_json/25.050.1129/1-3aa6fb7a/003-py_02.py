"""
The transformation preserves three azure (color 8) objects from the input grid to the output grid.
It adds a blue pixel (color 1) to mark specific corners on those objects.
"""

import numpy as np

def find_objects(grid, color):
    """Finds objects of a specific color in the grid."""
    objects = []
    visited = set()

    def dfs(r, c, current_object):
        """Depth-first search to find contiguous regions."""
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    azure_objects = find_objects(input_grid, 8)

    # Sort objects based on their topmost and then leftmost coordinate
    azure_objects.sort(key=lambda obj: (min(r for r, c in obj), min(c for r, c in obj)))

    #process objects
    
    if len(azure_objects) >= 1:
        first_object = azure_objects[0]
        topmost_pixel = min(first_object, key=lambda p: p[0])
        if topmost_pixel[1] > 0: #only if it's possible
          output_grid[topmost_pixel[0], topmost_pixel[1] - 1] = 1

    if len(azure_objects) >= 2:
        second_object = azure_objects[1]
        topmost_pixel = min(second_object, key=lambda p: p[0])
        if topmost_pixel[1]< output_grid.shape[1]-1: #check boundaries
            output_grid[topmost_pixel[0], topmost_pixel[1] + 1] = 1

    if len(azure_objects) >= 3:
        third_object = azure_objects[2]
        topmost_pixel = min(third_object, key=lambda p: p[0])
        if topmost_pixel[1] > 0:
          output_grid[topmost_pixel[0], topmost_pixel[1] -1] = 1
          
    return output_grid