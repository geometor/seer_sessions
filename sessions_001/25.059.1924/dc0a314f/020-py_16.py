"""
1. Identify Objects: Find all contiguous regions (objects) of the same color in the input grid.
2. Select Object: If there is exactly one object in the grid, select it.
3. Copy Object: Create a new grid with dimensions 5x5. Copy the selected object into the new grid, preserving its shape and color. The position of the copied object in the output grid matches the column of the object in the input grid. The object is placed starting at the top row of the output.
"""

import numpy as np

def get_objects(grid):
    """
    Identify contiguous blocks of the same color as objects.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                if obj:
                    objects.append(obj)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((5, 5), dtype=int)

    # find objects in the input grid
    objects = get_objects(input_grid)

    # select object if there is exactly one
    if len(objects) == 1:
        selected_object = objects[0]

        # copy the selected object to the output grid
        for row, col in selected_object:
            output_grid[row - min(r for r, _ in selected_object), col] = input_grid[row, col]

    return output_grid