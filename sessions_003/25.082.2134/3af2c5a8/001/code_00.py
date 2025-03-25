"""
The transformation rule is a combination of mirroring and duplication of objects to produce an output grid that is twice the size of the input in each dimension.
"""

import numpy as np

def find_objects(grid):
    # Find contiguous non-zero blocks of the same color.
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                obj = []
                dfs(r, c, grid[r][c], obj)
                objects.append((grid[r][c], obj))  # Store color and object
    return objects

def transform(input_grid):
    # Initialize output_grid with double the dimensions, filled with 0s.
    input_rows, input_cols = len(input_grid), len(input_grid[0])
    output_rows, output_cols = 2 * input_rows, 2 * input_cols
    output_grid = [[0] * output_cols for _ in range(output_rows)]

    # Find objects in input
    objects = find_objects(input_grid)


    # Mirror and duplicate objects.
    for color, obj in objects:
        for r, c in obj:
          # top-left
          output_grid[r][c] = color
          # top-right
          output_grid[r][output_cols - 1 - c] = color
          # bottom-left
          output_grid[output_rows - 1- r][c] = color
          # bottom-right
          output_grid[output_rows - 1 - r][output_cols - 1- c] = color

    return output_grid