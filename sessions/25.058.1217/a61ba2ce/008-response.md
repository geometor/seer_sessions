# a61ba2ce • 008 • refine_coder

---
```python
"""
Transforms objects in the input grid into horizontal lines or single pixels in the output grid. Horizontal lines in the input remain unchanged. Vertical lines become single pixels. Rectangles become horizontal lines with the same width as the original rectangle. The output grid is always 10x2.
"""

import numpy as np

def _find_objects(grid):
    """Finds contiguous blocks of non-zero pixels."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def _dfs(row, col, color, obj_coords):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        obj_coords.append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            _dfs(row + dr, col + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj_coords = []
                _dfs(r, c, grid[r, c], obj_coords)
                if obj_coords:
                  min_r = min(coord[0] for coord in obj_coords)
                  min_c = min(coord[1] for coord in obj_coords)
                  max_r = max(coord[0] for coord in obj_coords)
                  max_c = max(coord[1] for coord in obj_coords)

                  objects.append({
                      'color': grid[r, c],
                      'coords': obj_coords,
                      'top_left':(min_r,min_c),
                      'rows': max_r-min_r+1,
                      'cols': max_c-min_c+1
                  })
    return objects

def transform(input_grid):
    # Initialize the output grid
    output_grid = np.zeros((2, 10), dtype=int)

    # Find objects in the input grid
    objects = _find_objects(np.array(input_grid))

    # Place objects into the output grid
    for obj in objects:
        if obj['rows'] == 1 and obj['cols'] > 1:  # Horizontal line
            for i, (row, col) in enumerate(obj['coords']):
              if i < 10:
                output_grid[0, i] = obj['color']
        elif obj['cols'] == 1 and obj['rows'] > 1: # Vertical line
            output_grid[0, 0] = obj['color']
        elif obj['rows'] > 1 and obj['cols'] > 1:   # Rectangle
           for i in range(obj['cols']):
             if i < 10:
               output_grid[0,i] = obj['color']


    return output_grid.tolist()
```
