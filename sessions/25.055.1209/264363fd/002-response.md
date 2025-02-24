# 264363fd • 002 • example_1 • investigate_coder

---
```python
"""
The transformation identifies blue (1) regions within an azure (8) background and highlights specific parts of these regions. It creates an "inner border" within each blue region using red (2) pixels. Additionally, it highlights "corners" of these blue regions with green (3).
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the specified color.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj = []
                stack = [(r, c)]
                while stack:
                    curr_r, curr_c = stack.pop()
                    if 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == color and not visited[curr_r, curr_c]:
                        visited[curr_r, curr_c] = True
                        obj.append((curr_r, curr_c))
                        stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c),
                                      (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                objects.append(obj)
    return objects

def is_corner(grid, r, c, obj):
  """Checks if a pixel is a corner within the object 'obj'.  A corner is
  defined here as a pixel that is part of the object and is adjacent to
  at least one pixel that is not a part of the object.

  """
  rows, cols = grid.shape
  count = 0
  for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      nr, nc = r + dr, c + dc
      if 0 <= nr < rows and 0 <= nc < cols:
          if (nr, nc) not in obj:
              count = count +1
  return count >= 1

def get_inner_border(obj):
    """
    Returns the inner border of a blue object as set of coordinates.

    Args:
        obj: A list of (row, col) tuples representing the blue object.
        
    Returns: Set of coordinates that identify an inner border of the obj.
    """
    min_row = min(r for r, _ in obj)
    max_row = max(r for r, _ in obj)
    min_col = min(c for _, c in obj)
    max_col = max(c for _, c in obj)

    inner_border = set()

    for r, c in obj:
        # Check if the pixel is on the outer boundary
        if r == min_row or r == max_row or c == min_col or c == max_col:
          if r > min_row:
            inner_border.add((r - 1,c))
          if r < max_row:
            inner_border.add((r + 1, c))
          if c > min_col:
            inner_border.add((r,c - 1))
          if c < max_col:
            inner_border.add((r, c + 1))
            
    # remove duplicates by converting obj to a set
    obj_set = set(obj)
    inner_border = list(inner_border & obj_set)

    return inner_border

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find blue objects.
    blue_objects = find_objects(input_grid, 1)

    # Create inner borders and highlight corners.
    for obj in blue_objects:
        inner_border = get_inner_border(obj)
        for r, c in inner_border:
          # find corners and change color to 3
          if is_corner(input_grid, r, c, obj):
              output_grid[r, c] = 3
          else:
              output_grid[r,c] = 2

    return output_grid
```
