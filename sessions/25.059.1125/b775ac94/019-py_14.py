"""
The transformation rule constructs the output grid based on the positions and colors of objects in the input grid.  Specifically, it expands a blue (color 1) object to a 3x3 square at the top right, mirrors an azure (color 8) object to the right edge, extends a yellow (color 4) object to the right edge, extends a magenta (color 6) object by one to the right, and replicates a red object to a 3x3 block.

"""

import numpy as np

def find_objects(grid):
    """Finds distinct colored regions (objects) in the grid."""
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    objects = find_objects(input_grid)

    # Expand blue object (color 1) to top right
    if 1 in objects:
        for obj in objects[1]:
            min_row = min(r for r, c in obj)
            min_col = min(c for r, c in obj)  # Not actually needed for the top-right placement

            for r in range(max(0, min_row -2), min_row + 1 ): # 3 rows high
                for c in range(output_grid.shape[1] - 3, output_grid.shape[1]): # 3 columns wide, right edge
                  if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                      output_grid[r,c] = 1

    #Mirror azure (color 8)
    if 8 in objects:
      for obj in objects[8]:
          min_row = min(r for r,c in obj)
          max_row = max(r for r, c in obj)
          min_col = min(c for r,c in obj)
          max_col = max(c for r, c in obj)

          width = max_col - min_col + 1
          height = max_row - min_row + 1

          for r in range(min_row, max_row +1):
            for c in range(output_grid.shape[1] - width, output_grid.shape[1]):
                if 0 <= r < output_grid.shape[0]:
                  output_grid[r,c] = 8

    #Expand yellow (color 4)
    if 4 in objects:
        for obj in objects[4]:
            min_row = min(r for r,c in obj)
            max_row = max(r for r,c in obj)
            min_col = min(c for r,c in obj)

            for r in range(min_row, max_row+1):
                for c in range(min_col, output_grid.shape[1]):
                    output_grid[r,c] = 4

    #Expand magenta (color 6)
    if 6 in objects:
      for obj in objects[6]:
        for r,c in obj:
          if c+1 < output_grid.shape[1]:
            output_grid[r, c+1] = 6
            
    # replicate red to 3x3 block
    if 2 in objects:
        for obj in objects[2]:
            min_row = min(r for r, c in obj)
            min_col = min(c for r, c in obj)

            for r in range(min_row, min(min_row + 3, output_grid.shape[0])):
                for c in range(min_col, min(min_col + 3, output_grid.shape[1])):
                  output_grid[r, c] = 2
    return output_grid