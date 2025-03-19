"""
The transformation rule is as follows:

1. Identify Objects: Divide all the colored objects (non-white pixels) in the input grid into two sets. Call the first set "set A" and the second set "set B."
2.  **Object Replacement**: Delete set A objects and re-draw set B objects.
3. The output grid will be identical to the input grid, but with one set of objects being replaced with another set of objects.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in a grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_coords = []
                dfs(row, col, grid[row, col], obj_coords)
                objects.append(obj_coords)
    return objects


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find all objects
    objects = find_objects(input_grid)
    
    if len(objects) < 2:
       return output_grid
      
    set_a = objects[0]
    set_b = objects[1]
        
    # replace set A with B and B with A
    # first set
    for row, col in set_b:
          output_grid[row,col] = input_grid[row,col]

    # second set 
    for row, col in set_a:
          output_grid[row,col] = input_grid[row,col]

    # fill output with set B and Set A
    return output_grid