"""
Identify all objects in the input grid. Identify vertical lines within the set of objects. Extract the detected vertical line. Output the extracted vertical line as a grid.
"""

import numpy as np

def find_objects(grid):
    # Find contiguous regions of non-zero pixels
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
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
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if not visited[i, j] and grid[i, j] != 0:
                obj = []
                dfs(i, j, grid[i, j], obj)
                objects.append(obj)
    return objects

def is_vertical_line(obj, grid):
    # Check if an object is a vertical line
    if not obj:
        return False
    
    rows, cols = zip(*obj)
    min_col, max_col = min(cols), max(cols)
    min_row, max_row = min(rows), max(rows)

    if max_col - min_col == 0 and max_row - min_row +1 == len(obj):
      return True
    else:
      return False
    

def transform(input_grid):
    # Find all objects in the grid
    objects = find_objects(input_grid)
    
    # Select any vertical line
    selected_object = None
    for obj in objects:
        if is_vertical_line(obj, input_grid):
            selected_object = obj
            break
    
    # Initialize output grid (Handle case where the object isn't found)
    if selected_object:
      rows, _ = zip(*selected_object)
      min_row, max_row = min(rows), max(rows)
      color = input_grid[selected_object[0][0], selected_object[0][1]]
      output_grid = np.full((max_row - min_row + 1, 1), color)

    else:
      output_grid = np.array([]) #return empty array

    return output_grid