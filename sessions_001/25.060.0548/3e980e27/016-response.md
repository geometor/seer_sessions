# 3e980e27 • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate all contiguous blocks of non-white pixels. Each block, regardless of size, is considered an object.  Assign unique IDs to all objects based on color and location.

2.  **Vertical Mirroring/Shifting:**
    *   Imagine a vertical axis somewhere near the center of the grid (possibly column-dependent, need to test).
    *   Duplicate objects and swap locations across the hypothetical vertical axis line.
    * It looks like some of the colored objects on the right side of the output grid, look like duplicates from other colored objects on the left, and some colored objects on the left have moved down.

3.  **Combine:** Combine duplicated and original objects into the output grid
"""

import numpy as np

def find_objects(grid):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append({"color": grid[r, c], "coords": obj_coords})
    return objects

def reflect_point(point, axis, max_val):
    """Reflects a single point across a given axis."""
    r, c = point
    if axis == 'vertical':
        dist_to_axis = axis - c
        new_c = axis + dist_to_axis
        if new_c >= max_val: # Handle reflections that go out of bounds.
             return None
        return (r, new_c)
    return None # Not handling horizontal for this task

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    objects = find_objects(input_grid)

    vertical_axis = 6  # Hypothesis: Vertical axis for reflection

    for obj in objects:
      color = obj['color']
      for coord in obj['coords']:
          # if left of vertical axis, duplicate, shift down and right
          if coord[1] < vertical_axis:
            if color == 3 or color == 8:
               reflected_coord = reflect_point(coord, vertical_axis, cols)
               if reflected_coord:
                  output_grid[reflected_coord[0]+1, reflected_coord[1]] = 4
            
          # if right of vertical axis, duplicate shift up
          if coord[1] >= vertical_axis:
              if (color == 2 and coord[1] == 10) or (color == 4 and coord[1] == 6):
                 reflected_coord = reflect_point(coord, vertical_axis, cols)
                 if reflected_coord:
                    output_grid[reflected_coord[0]-1, reflected_coord[1]] = color
    
    return output_grid
```
