"""
The input grid is analyzed to identify distinct objects, where an object is a contiguous block of pixels of the same color.
For each object in the input grid:
    1. Determine the object's bounding box (min/max row and column).
    2. Calculate the object's width and height.
    3. Replicate the object's pixels to the left, right, above, and below the original object, at a distance equal to the object's width and height, respectively. The original object's position is unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append((grid[r,c], obj))
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the replication rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(input_grid)  # Initialize with input grid
    rows, cols = input_grid.shape

    objects = find_objects(input_grid)

    for color, obj in objects:
        # Find bounding box of the object
        min_r = min(r for r, c in obj)
        max_r = max(r for r, c in obj)
        min_c = min(c for r, c in obj)
        max_c = max(c for r, c in obj)

        obj_height = max_r - min_r + 1
        obj_width = max_c - min_c + 1

        # Replicate horizontally and vertically
        for r, c in obj:
            # Copy to the left
            left_c = c - obj_width
            if left_c >= 0:
                output_grid[r, left_c] = color

            # Copy to the right
            right_c = c + obj_width
            if right_c < cols:
                output_grid[r, right_c] = color

            # Copy to the top
            top_r = r - obj_height
            if top_r >= 0:
                output_grid[top_r, c] = color

            # Copy to the bottom
            bottom_r = r + obj_height
            if bottom_r < rows:
                output_grid[bottom_r, c] = color
    
    return output_grid