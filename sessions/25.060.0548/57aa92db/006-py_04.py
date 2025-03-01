"""
The transformation rule is as follows:
1. If there are any blue pixels, remove all of them.
2.  Expand the yellow region.  If the yellow region is on a single row, add
yellow above or below.  If there are multiple rows of yellow, do not expand
yellow.
"""

import numpy as np

def get_objects(grid):
    """
    Identify contiguous regions of the same color as distinct objects.
    Returns a dictionary of objects keyed by color.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
            visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                color = grid[row, col]
                obj_pixels = []
                dfs(row, col, color, obj_pixels)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_pixels)
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()
    objects = get_objects(input_grid)

    # 1. remove all blue pixels
    if 1 in objects:
      for blue_object in objects[1]:
        for pixel in blue_object:
          output_grid[pixel] = 0
          
    # 2. Expand yellow region vertically based on condition
    if 4 in objects:
      for yellow_object in objects[4]:
          # Find min and max row indices for the yellow region
          rows = [pixel[0] for pixel in yellow_object]
          min_row = min(rows)
          max_row = max(rows)

          if min_row == max_row: # Only expand if yellow is on a single row
              # Expand up if possible
              if min_row > 0:
                  for col in range(input_grid.shape[1]):
                      if (min_row-1,col) not in yellow_object:
                        if input_grid[min_row-1,col] == 0:
                          output_grid[min_row - 1, col] = 4
              # Expand down if possible
              if max_row < input_grid.shape[0] - 1:
                  for col in range(input_grid.shape[1]):
                    if (max_row+1,col) not in yellow_object:
                      if input_grid[max_row+1,col] == 0:
                        output_grid[max_row + 1, col] = 4

    return output_grid