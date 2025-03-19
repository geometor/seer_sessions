# 90c28cc7 • 014 • refine_coder

---
```python
"""
Identifies distinct colored rectangular regions within the input grid, extracts their colors, and creates a minimal-sized output grid containing these colors.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all distinct, contiguous, rectangular regions of non-zero colored pixels.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def dfs(r, c, color, min_row, min_col, max_row, max_col):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        min_row[0] = min(min_row[0], r)
        min_col[0] = min(min_col[0], c)
        max_row[0] = max(max_row[0], r)
        max_col[0] = max(max_col[0], c)

        dfs(r + 1, c, color, min_row, min_col, max_row, max_col)
        dfs(r - 1, c, color, min_row, min_col, max_row, max_col)
        dfs(r, c + 1, color, min_row, min_col, max_row, max_col)
        dfs(r, c - 1, color, min_row, min_col, max_row, max_col)


    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                min_row, min_col, max_row, max_col = [r], [c], [r], [c]
                dfs(r, c, grid[r, c], min_row, min_col, max_row, max_col)
                #check if it is rectangular
                is_rectangle = True
                for rr in range(min_row[0], max_row[0] + 1):
                  for cc in range(min_col[0], max_col[0]+1):
                    if grid[rr,cc] != grid[r,c]:
                      is_rectangle = False
                      break
                  if not is_rectangle:
                    break

                if is_rectangle:
                  objects.append({
                      "color": grid[r, c],
                      "min_row": min_row[0],
                      "min_col": min_col[0],
                      "max_row": max_row[0],
                      "max_col": max_col[0]
                  })
    return objects

def transform(input_grid):
    # Find distinct colored rectangular regions (objects)
    objects = find_objects(np.array(input_grid))

    # Extract colors from the objects
    colors = [obj["color"] for obj in objects]
    num_colors = len(colors)

    # Create output grid based on the number of distinct colors
    if num_colors == 1:
        output_grid = np.array([[colors[0]]])
    elif num_colors == 2:
        #order by x coordinate
        if objects[0]["min_col"] < objects[1]["min_col"]:
          output_grid = np.array([[colors[0], colors[1]]])
        else:
          output_grid = np.array([[colors[1], colors[0]]])

    elif num_colors == 4:
        output_grid = np.zeros((2, 2), dtype=int)
        # Sort objects based on their top-left corner coordinates.
        sorted_objects = sorted(objects, key=lambda obj: (obj["min_row"], obj["min_col"]))
        output_grid[0, 0] = sorted_objects[0]["color"]
        output_grid[0, 1] = sorted_objects[1]["color"]
        output_grid[1, 0] = sorted_objects[2]["color"]
        output_grid[1, 1] = sorted_objects[3]["color"]

    else: # other shapes not defined
        output_grid = np.zeros((1,1), dtype=int)

    return output_grid
```
