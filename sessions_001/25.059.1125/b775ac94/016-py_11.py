"""
1.  **Identify Objects:** Locate all distinct colored regions (objects) in the input grid. These are contiguous areas of non-zero pixels.
2.  **Expansion and Mirroring, part 1:**
    *   Locate the blue object (color 1). Expand the blue object into a 3x3 square, by adding one pixel above the "1", and two to the right, maintaining blue (color 1)
    *   Locate the two azure pixels at the top, and copy a 2x1 block to the right edge of the grid.
3.  **Expansion and Mirroring, part 2:**
    * Locate the red object (color 2) at the bottom of the image and extend the horizontal yellow bar (color 4) to the right edge, adding two yellow (color 4) pixels.
4. **Expansion and Mirroring part 3:**
    * Locate the magenta pixel (color 6). Add an adjacent magenta pixel (color 6) to the right.
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
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Expand blue object (color 1)
    if 1 in objects:
        for obj in objects[1]:
          #find "center" of object
            min_row = min(r for r, c in obj)
            min_col = min(c for r, c in obj)

            for r in range(min_row -1, min_row + 2):
                for c in range(min_col, min_col + 3):
                    if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                      output_grid[r,c] = 1

    #Mirror azure
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
              output_grid[r,c] = 8

    #Expand yellow
    if 4 in objects:
        for obj in objects[4]:
            min_row = min(r for r,c in obj)
            max_row = max(r for r,c in obj)
            min_col = min(c for r,c in obj)

            for r in range(min_row, max_row+1):
                for c in range(min_col, output_grid.shape[1]):
                    output_grid[r,c] = 4

    #Expand magenta
    if 6 in objects:
      for obj in objects[6]:
        for r,c in obj:
          if c+1 < output_grid.shape[1]:
            output_grid[r, c+1] = 6
    return output_grid