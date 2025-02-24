"""
1.  **Top-Left Object Modification:** Identify the top-most green (3) object in the input grid.  If a cell within this object is green (3) and is directly above a red (2) cell, change the green cell to white (0).
2.  **Bottom-Right Object Extension:** Identify the bottom-most green (3) object. Add red (2) pixels to the left of the bottom-most green object. The added red pixels form a column or columns that extend upward to the row index of the top-most green object.  If the bottom most object is taller (has more rows) than the upper object, then the red extension will be adjacent, but will only be the same height as the top green object.
"""

import numpy as np

def find_objects(grid, color):
    # Find objects of a specific color in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_object_bounds(obj):
    # Get the bounding box of an object.
    rows, cols = zip(*obj)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find green objects
    green_objects = find_objects(input_grid, 3)
    
    # Identify top-most and bottom-most green objects
    if not green_objects:
        return output_grid

    top_green = sorted(green_objects, key=lambda obj: get_object_bounds(obj)[0])[0]
    bottom_green = sorted(green_objects, key=lambda obj: get_object_bounds(obj)[0])[-1]

    top_bounds = get_object_bounds(top_green)
    bottom_bounds = get_object_bounds(bottom_green)


    # 1. Top-Left Object Modification
    for r in range(top_bounds[0], top_bounds[1] + 1):
        for c in range(top_bounds[2], top_bounds[3] + 1):
            if (r,c) in top_green and r + 1 < input_grid.shape[0] and input_grid[r+1, c] == 2:
                output_grid[r, c] = 0

    # 2. Bottom-Right Object Extension
    min_row_top = top_bounds[0]
    extension_height = (bottom_bounds[1] - bottom_bounds[0] +1)
    
    red_col = bottom_bounds[2] - 1
    for row in range(min_row_top, min_row_top + extension_height):
      if row < output_grid.shape[0] and red_col >= 0:
        output_grid[row, red_col] = 2

    return output_grid