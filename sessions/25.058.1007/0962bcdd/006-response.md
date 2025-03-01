# 0962bcdd • 006 • refine_coder

---
```python
"""
1.  **Identify Plus Shapes:** Locate all "plus-shaped" objects in the input grid. A plus-shaped object consists of orange (7) pixels forming a plus sign, with a single red (2) pixel at its center.

2.  **Expand Plus Shapes:** For each identified plus shape, expand it outwards to create a hollow rectangular or square shape. The outline of this expanded shape should still consist of orange (7) pixels, except where the original red (2) center pixel was located.

3.  **Fill with Red:** Fill the entire area between the expanded shapes, up to and including their outer boundaries (where not already occupied by orange (7) pixels), with red (2) pixels. This creates a single, contiguous red (2) region encompassing and connecting the expanded plus shapes. The result is a single area of red, where there were gaps now the area is filled in.
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

def fill_between(grid, expanded_objects):
    """Fills the area between and including expanded objects with red (2)."""
    rows, cols = grid.shape
    min_r, min_c = rows, cols
    max_r, max_c = 0, 0

    # Find the overall bounding box
    for obj in expanded_objects:
        for r, c in obj:
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)
    
    # Fill everything within the bounding box with red, except existing oranges
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r,c] != 7:  # Don't overwrite expanded orange parts
               grid[r,c] = 2

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    grid = np.array(input_grid)
    output_grid = np.copy(grid)

    # 1. Find plus-shaped objects
    plus_objects = find_plus_objects(grid)

    # 2. Expand the plus-shapes
    expanded_objects = []
    for obj in plus_objects:
        expanded = expand_plus(grid, obj)
        expanded_objects.append(expanded)
        for r, c in expanded:
          if output_grid[r,c] != 2:  # keep the original center
            output_grid[r, c] = 7
    

    # 3. Fill between expanded objects
    if expanded_objects: # make sure list isn't empty
       fill_between(output_grid, expanded_objects)

    return output_grid
```
