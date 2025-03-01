"""
The transformation identifies distinct objects in the input grid and stacks them vertically in the output grid. The stacking order is determined by the horizontal position of the objects in the input grid, from left to right. The objects maintain their original shapes and sizes. Background (white/0) pixels are removed to eliminate empty rows.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all distinct objects in the grid.
    Returns a list of (object, top_left) tuples.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, object_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                if object_pixels:
                    # Find top-left coordinate of the object
                    top_left = (min(p[0] for p in object_pixels), min(p[1] for p in object_pixels))
                    # create object using a minimal bounding box
                    obj_rows, obj_cols = zip(*object_pixels)
                    obj_height = max(obj_rows) - min(obj_rows) + 1
                    obj_width = max(obj_cols) - min(obj_cols) + 1
                    obj = np.zeros((obj_height, obj_width), dtype=int)
                    for r, c in object_pixels:
                        obj[r - top_left[0], c - top_left[1]] = grid[r, c]
                    objects.append((obj, top_left))

    return objects

def remove_empty_rows(grid):
    """Removes rows that are entirely filled with 0s."""
    non_empty_rows = np.any(grid != 0, axis=1)
    filtered_grid = grid[non_empty_rows]
    return filtered_grid

def transform(input_grid):
    # Find all objects
    objects = find_objects(input_grid)

    # Sort objects by their top-left x-coordinate (column)
    objects.sort(key=lambda x: x[1][1])

    # initialize output_grid with the correct dimensions, filled with 0s.
    # It is difficult to know the correct dimension before processing all the
    # objects so we will start large
    output_grid = np.zeros((30, 30), dtype=int)

    # Stack objects vertically
    current_row = 0
    for obj, _ in objects:
        height, width = obj.shape
        output_grid[current_row:current_row + height, 0:width] = obj
        current_row += height

    #remove white space
    output_grid = remove_empty_rows(output_grid)
    return output_grid