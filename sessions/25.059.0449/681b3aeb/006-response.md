# 681b3aeb • 006 • refine_coder

---
```python
"""
1.  **Identify and Count:** Identify all distinct colored objects (contiguous regions of the same color) in the input grid. Count the number of pixels for each color, specifically green (3) and orange (7).
2.  **Create Output Grid:** The output is always a 3x3 grid.
3.  **Conditional Placement:**
    *   If the sum of green and orange pixels is less than or equal to 3: Place all green pixels in the first column of the output grid, starting from the top. Place all orange pixels in the third column of the output grid, starting from the top. Fill the rest of the columns with black (0) pixels.
    * If the number of green pixels is exactly 1 and the number of orange pixels is exactly 2. Place all green pixels in the first column and all orange pixels in the third column. Fill the rest of the columns with black(0) and perform a 90-degree counter-clockwise rotation on the grid.
"""

import numpy as np

def get_objects(grid):
    """Finds distinct connected components in the grid."""
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj_id):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        objects[obj_id].append((r, c))
        dfs(r + 1, c, color, obj_id)
        dfs(r - 1, c, color, obj_id)
        dfs(r, c + 1, color, obj_id)
        dfs(r, c - 1, color, obj_id)

    obj_id = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                objects[obj_id] = []
                dfs(r, c, grid[r, c], obj_id)
                obj_id += 1
    return objects

def count_colors(input_grid, colors=[3, 7]):
    """Counts the occurrences of specified colors in the grid."""
    counts = {color: 0 for color in colors}
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] in colors:
                counts[input_grid[r, c]] += 1
    return counts

def rotate_grid(grid):
    """Rotates a grid 90 degrees counter-clockwise."""
    return np.rot90(grid)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Count green and orange pixels
    color_counts = count_colors(input_grid)
    green_count = color_counts[3]
    orange_count = color_counts[7]


    # Place objects into output grid based on counts
    if green_count + orange_count <= 3:
      green_placed = 0
      orange_placed = 0
      objects = get_objects(input_grid)
      for obj_id, pixels in objects.items():
          color = input_grid[pixels[0]]
          if color == 3:
              for i in range(len(pixels)):
                  if green_placed < 3:
                    output_grid[green_placed, 0] = 3
                    green_placed++
          elif color == 7:
              for i in range(len(pixels)):
                  if orange_placed < 3:
                    output_grid[orange_placed, 2] = 7
                    orange_placed++
    
    if green_count == 1 and orange_count == 2:
        output_grid = rotate_grid(output_grid)
        

    return output_grid
```
