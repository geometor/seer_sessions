"""
The transformation extracts a subregion from the input grid, focusing on the relative positions of a large red rectangle and a smaller yellow shape. A bounding box is created around the yellow shape, extended, and then enclosed within a red border in the output grid.
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct objects in the grid.
    Returns a dictionary of objects, where keys are colors and values are lists of pixel coordinates.
    """
    objects = {}
    visited = set()

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if (r, c) not in visited and grid[r,c]!=0:
                color = grid[r, c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)

    return objects


def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    # Find objects in the grid
    objects = find_objects(input_grid)

    # Find the bounding box for the yellow object (color 4)
    yellow_coords = []

    if 4 in objects:
      for obj_list in objects[4]:
        yellow_coords.extend(obj_list)
    
    if not yellow_coords:
        # handle edge case
        max_y = input_grid.shape[0] -1
        max_x = input_grid.shape[1] - 1
        output_grid = np.zeros((11,11), dtype=int)
        output_grid[0,:] = 2
        output_grid[10,:] = 2
        output_grid[:,0] = 2
        output_grid[:,10] = 2

        return output_grid
      
    min_r = min(r for r, c in yellow_coords)
    max_r = max(r for r, c in yellow_coords)
    min_c = min(c for r, c in yellow_coords)
    max_c = max(c for r, c in yellow_coords)

    # Extend the bounding box
    min_r = max(0, min_r - 1)
    max_r = max_r + 1
    min_c = max(0, min_c - 2)
    max_c = max_c + 2

    # Create the output grid with extended dimensions
    output_height = max_r - min_r + 3  # +3 for the border
    output_width = max_c - min_c + 3 # +2 for left/right, +1 more

    output_grid = np.zeros((output_height, output_width), dtype=int)


    # Place the yellow object within the output grid
    for r, c in yellow_coords:
        output_grid[r - min_r + 1, c - min_c + 1] = 4


    # Add the red border (color 2)
    output_grid[0, :] = 2
    output_grid[-1, :] = 2
    output_grid[:, 0] = 2
    output_grid[:, -1] = 2

    return output_grid