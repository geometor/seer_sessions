"""
Copies the input grid to the output grid. Then, it swaps the colors of blue (1) shapes to red (2) and red (2) shapes to blue (1), keeping other colors unchanged.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous objects of a specific color in the grid.
    visited = set()
    objects = []

    def dfs(r, c, current_object):
        if (r, c) in visited or r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or grid[r, c] != color:
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
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find blue objects and change to red
    blue_objects = find_objects(input_grid, 1)
    for obj in blue_objects:
        for r, c in obj:
            output_grid[r, c] = 2

    # Find red objects and change to blue
    red_objects = find_objects(input_grid, 2)
    for obj in red_objects:
        for r, c in obj:
            output_grid[r, c] = 1
            
    return output_grid