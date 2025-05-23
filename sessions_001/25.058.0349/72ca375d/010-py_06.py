"""
1.  Identify all 2x2 yellow squares in the input grid.
2.  Select any one of the 2x2 square.
3.  Extract the selected 2x2 yellow square object.
4.  The extracted square object becomes the output grid. All other regions are discarded.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = set()

    def dfs(row, col):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []

        visited.add((row, col))
        object_pixels = [(row, col)]

        object_pixels.extend(dfs(row + 1, col))
        object_pixels.extend(dfs(row - 1, col))
        object_pixels.extend(dfs(row, col + 1))
        object_pixels.extend(dfs(row, col - 1))

        return object_pixels

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                objects.append(dfs(row, col))

    return objects


def get_object_bounds(object_pixels):
    min_row = min(p[0] for p in object_pixels)
    max_row = max(p[0] for p in object_pixels)
    min_col = min(p[1] for p in object_pixels)
    max_col = max(p[1] for p in object_pixels)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find all yellow objects
    yellow_objects = find_objects(input_grid, 4)

    # Find all 2x2 yellow squares
    target_objects = []
    for obj in yellow_objects:
        min_row, max_row, min_col, max_col = get_object_bounds(obj)
        if (max_row - min_row + 1) == 2 and (max_col - min_col + 1) == 2:
            target_objects.append(obj)

    # Extract the first 2x2 yellow square, if any.
    if target_objects:
        min_row, max_row, min_col, max_col = get_object_bounds(target_objects[0])
        output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
        return output_grid

    return None