"""
The transformation rule involves identifying objects of the same color, combining them, potentially mirroring them, and then constructing the output grid.
Specifically, for each color in the input, the corresponding object is expanded in all four directions (up, down, left, and right), as if mirrored, creating a larger object of that same color.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies distinct objects in the grid.
    """
    objects = {}
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c, color, obj_id):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != color:
            return []
        visited.add((r, c))
        coords = [(r, c)]
        coords.extend(dfs(r + 1, c, color, obj_id))
        coords.extend(dfs(r - 1, c, color, obj_id))
        coords.extend(dfs(r, c + 1, color, obj_id))
        coords.extend(dfs(r, c - 1, color, obj_id))
        return coords

    obj_id = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r][c] != 0:
                color = grid[r][c]
                obj_coords = dfs(r, c, color, obj_id)
                objects[obj_id] = {'color': color, 'coords': obj_coords}
                obj_id += 1
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the mirroring rule.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    objects = get_objects(input_grid)

    for obj_id, obj_data in objects.items():
        color = obj_data['color']
        coords = obj_data['coords']

        # Combine and mirror
        for r, c in coords:
            output_grid[r, c] = color
            # "Mirror" by expanding in all directions.
            for i in range(rows):
                output_grid[i,c] = color

            for j in range(cols):
                output_grid[r,j] = color

    return output_grid.tolist()