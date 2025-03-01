"""
The input grid is analyzed to identify distinct objects. An object is defined as a contiguous block of pixels of the same color.
For each object:
    Find the bounding box of the object (min/max rows and cols).
    For each pixel in object
        copy the pixel value to the left by obj_width, mirroring its original location.
        copy the pixel value to the right by obj_width, mirroring its original location.
        copy the pixel value to the top by obj_height, mirroring its original location.
        copy the pixel value to the bottom by obj_height, mirroring its original location.
The output grid is formed by these replications, creating a symmetrical pattern expanding outward from each object.
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
    output_grid = np.zeros_like(input_grid)
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

        # Replicate horizontally and vertically, keeping original pixels
        for r, c in obj:
            output_grid[r, c] = color  # Keep original pixel

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