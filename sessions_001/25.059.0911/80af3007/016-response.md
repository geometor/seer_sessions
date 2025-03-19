# 80af3007 • 016 • refine_coder

---
```python
"""
The transformation extracts gray (5) shapes from the input grid and redraws them, scaled down, into a 9x9 output grid. The shapes and relative positions of the gray objects are preserved during the scaling.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the specified color
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
                        stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c), (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                objects.append(obj)
    return objects

def get_bounding_box(obj):
    # Calculate the bounding box of an object
    min_r = min(r for r, c in obj)
    max_r = max(r for r, c in obj)
    min_c = min(c for r, c in obj)
    max_c = max(c for r, c in obj)
    return (min_r, min_c, max_r, max_c)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)

    # Find gray objects
    gray_objects = find_objects(input_grid, 5)

    # Calculate scaling factors
    scale_r = 9 / input_grid.shape[0]
    scale_c = 9 / input_grid.shape[1]

    # Extract and project pattern into smaller grid
    for obj in gray_objects:
        # Calculate bounding box
        min_r, min_c, max_r, max_c = get_bounding_box(obj)

        # Scale and redraw object
        for r, c in obj:
            # Calculate scaled coordinates relative to the bounding box, then scale the bounding box.
            scaled_r = int(min_r * scale_r + (r - min_r) * scale_r)
            scaled_c = int(min_c * scale_c + (c - min_c) * scale_c)

            # Check bounds (due to rounding, some coordinates might fall outside)
            if 0 <= scaled_r < 9 and 0 <= scaled_c < 9:
              output_grid[scaled_r, scaled_c] = 5

    return output_grid
```
