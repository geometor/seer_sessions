# 29623171 • 004 • example_1 • investigate_coder

---
```python
"""
Preserve gray lines, remove blue pixels not connected to gray at bottom right,
and create a 3x3 blue square at the bottom right, based on the horizontal
position of bottom gray elements.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)

    return objects

def get_bottom_gray_line_x(grid, gray_color=5):
    rows, cols = grid.shape
    for r in reversed(range(rows)):
      for c in reversed(range(cols)):
        if grid[r,c] == gray_color:
          return r,c
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Preserve Gray
    # find gray and blue objects
    # gray_objects = find_objects(input_grid, 5) # we know they are horizontal lines, so no need
    blue_objects = find_objects(input_grid, 1)

    # find bottom gray line right corner
    bottom_gray_row, bottom_gray_x = get_bottom_gray_line_x(input_grid)
    
    # Remove Isolated Blue not adjacent to right corner gray
    for blue_object in blue_objects:
      is_connected = False
      for r,c in blue_object:
        if (r+1 == bottom_gray_row and c == bottom_gray_x) or \
           (r-1 == bottom_gray_row and c == bottom_gray_x) or \
           (r == bottom_gray_row and c+1 == bottom_gray_x) or \
           (r == bottom_gray_row and c-1 == bottom_gray_x):

          is_connected = True
          break
      if not is_connected:
        for r,c in blue_object:
          output_grid[r,c] = 0
          
    # Create 3x3 Bottom Blue one line below bottom_gray_row
    if bottom_gray_row is not None:
      start_row = bottom_gray_row + 1
      start_col = bottom_gray_x -1  # Corrected column calculation
      
      for r in range(start_row, min(start_row + 3, rows)):
          for c in range(start_col, min(start_col + 3, cols)):
            if 0 <= r < rows and 0 <= c < cols: # ensure valid index
              output_grid[r, c] = 1

    return output_grid
```
