# a3325580 • 004 • refine_coder

---
```python
"""
The transformation identifies non-background (non-zero) colors in the input grid. The output grid contains columns representing each identified color. The height of the output grid is determined by finding rows that have matching colors.  If a column has no additional colors, pad with black.
"""

import numpy as np

def get_objects(grid):
    """
    Finds connected components (objects) in the grid.

    Returns a list of objects.  Each element of list is a
    list of (row,col) tuples of the non-background pixels.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_color_rows(grid):
    """
    Find rows that contain only one color, repeated.
    """
    rows, cols = grid.shape
    color_rows = []

    for r in range(rows):
        row_colors = []
        for c in range(cols):
            if grid[r,c] != 0:
               row_colors.append(grid[r,c])

        if len(row_colors) > 0:
          first_color = row_colors[0]
          all_same = True
          for color in row_colors:
            if color != first_color:
              all_same = False
              break

          if all_same:
            color_rows.append((r,first_color))

    return color_rows

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    objects = get_objects(input_grid)

    # find distinct non zero colors
    colors = sorted(list(set(input_grid.flatten())))
    colors = [c for c in colors if c!= 0]

    color_rows = get_color_rows(input_grid)

    output_rows = 0
    color_map = {}
    for r,color in color_rows:
      if color not in color_map:
         color_map[color] = []
      color_map[color].append(r)
      output_rows = max(output_rows, len(color_map[color]))

    # initialize the grid
    output_grid = np.zeros((output_rows, len(colors)), dtype=int)

    # populate the grid based on matching colors
    for j, color in enumerate(colors):
        if color in color_map:
          for i,row in enumerate(color_map[color]):
              output_grid[i,j] = color

    return output_grid.tolist()
```
