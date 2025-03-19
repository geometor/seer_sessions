# 0962bcdd • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify "plus-shaped" objects:** Find connected components of 'orange' (7) pixels in the input grid that form a plus shape, with a single 'red' (2) pixel in the center.

2.  **Expand the plus-shapes:** For each identified plus-shaped object, transform the orange (7) pixels into a hollow rectangle or square shape. The shape should expand outwards.

3.  **Connect the expanded shapes** Place 'red' (2) pixels between two shapes. These red pixels form two separate diagonals connecting all 4 corners of the original shapes.

4. Fill in the area between plus-shaped objects with lines of "red" (2). The "red" (2) lines fill the two newly formed diagnols.
"""

import numpy as np

def find_plus_objects(grid):
    """Finds plus-shaped objects (7s surrounding a 2)."""
    objects = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, obj):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] not in (2, 7):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, obj)
        dfs(r - 1, c, obj)
        dfs(r, c + 1, obj)
        dfs(r, c - 1, obj)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 7 and not visited[r, c]:
                obj = []
                dfs(r, c, obj)
                # Check if it's a plus shape with a 2 in the center
                if any(grid[row, col] == 2 for row, col in obj):
                   is_plus = True
                   center = None
                   for row,col in obj:
                       if grid[row,col] == 2:
                           if center is not None:
                               is_plus = False
                               break # only 1 center of 2 allowed
                           else:
                               center = (row,col)
                   if is_plus:
                        orange_neighbors = 0
                        if center:
                            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                                nr, nc = center[0] + dr, center[1] + dc
                                if is_valid(nr,nc) and grid[nr,nc] == 7:
                                     orange_neighbors += 1
                        if orange_neighbors == 4:
                            objects.append(obj)


    return objects

def expand_plus(grid, plus_object):
    """Expands the plus-shaped object into a hollow square."""
    # Find the bounding box of the plus object
    min_r, min_c = plus_object[0]
    max_r, max_c = plus_object[0]
    for r, c in plus_object:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)

    # Create the expanded hollow square
    expanded_object = []
    for r in range(min_r - 1, max_r + 2):
        for c in range(min_c - 1, max_c + 2):
            if (min_r -1 <= r <= max_r + 1) and (min_c - 1 <= c <= max_c+1):
                expanded_object.append((r, c))
    return expanded_object

def connect_shapes(grid, expanded_object1, expanded_object2):
   """Connects the two expanded shapes with lines of 2s"""
   min_r1, min_c1 = expanded_object1[0][0], expanded_object1[0][1]
   for r, c in expanded_object1:
      if r <= min_r1:
         min_r1 = r
      if c <= min_c1:
         min_c1 = c

   max_r2, max_c2 = expanded_object2[0][0], expanded_object2[0][1]
   for r, c in expanded_object2:
       if r >= max_r2:
           max_r2 = r
       if c >= max_c2:
           max_c2 = c


   # top left of first object
   #grid[min_r1-1, min_c1-1] = 2

   # top left to bottom right
   r, c = min_r1, min_c1
   while  r <= max_r2 and c <= max_c2:
       if not (r, c) in expanded_object1 and not (r, c) in expanded_object2:
            grid[r,c] = 2
       r += 1
       c += 1
   # bottom right of first object to top left of second object
   r, c = min_r1, max_c1
   while r <= max_r2 and c >= min_c2:
      if not (r,c) in expanded_object1 and not(r,c) in expanded_object2:
         grid[r,c] = 2
      r += 1
      c -= 1

   return

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.zeros_like(grid)  # Initialize output grid

    # 1. Find plus-shaped objects
    plus_objects = find_plus_objects(grid)

    # 2. Expand the plus-shapes
    expanded_objects = []
    for obj in plus_objects:
        expanded = expand_plus(grid, obj)
        expanded_objects.append(expanded)
        for r, c in expanded:
            output_grid[r,c] = 7

    # Put the 2's back after expanding
    for obj in plus_objects:
      for r,c in obj:
         if grid[r,c] == 2:
            output_grid[r,c] = 2


    # 3. Connect the expanded shapes (if there are two)
    if len(expanded_objects) == 2:
      connect_shapes(output_grid, expanded_objects[0], expanded_objects[1])


    return output_grid
```
