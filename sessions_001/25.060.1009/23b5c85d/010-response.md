# 23b5c85d • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Scan the input grid and identify all distinct rectangular objects based on contiguous blocks of the same color. Note color, size, and location.

2.  **Locate the target object:** Locate the blue colored object that is positioned at bottom right area of the input.

3. **Determine output size**: The size of the output grid is identical to the dimensions of the blue object in the input, but transposed, such as the blue rectangle is 2 by 3, and output 3 by 2.

4.  **Create Output:** Create an output grid of the determined size (from step 3), filled entirely with blue color (value 1).
"""

import numpy as np

def find_objects(grid):
    """Finds rectangular objects in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c, color):
        return 0 <= r < rows and 0 <= c < cols and grid[r, c] == color and (r, c) not in visited

    def dfs(r, c, color, object_coords):
        visited.add((r, c))
        object_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc, color):
                dfs(nr, nc, color, object_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r,c] != 0:
                color = grid[r, c]
                object_coords = []
                dfs(r, c, color, object_coords)
                if object_coords:
                    min_r = min(coord[0] for coord in object_coords)
                    max_r = max(coord[0] for coord in object_coords)
                    min_c = min(coord[1] for coord in object_coords)
                    max_c = max(coord[1] for coord in object_coords)
                    objects.append({
                        "color": color,
                        "position": (min_r, min_c),
                        "dimensions": (max_r - min_r + 1, max_c - min_c + 1)
                    })
    return objects

def transform(input_grid):
    # Find all objects in the grid
    objects = find_objects(input_grid)

    # Find the blue object
    blue_object = None
    for obj in objects:
        if obj['color'] == 1:
            blue_object = obj
            break

    # If no blue object is found, return an empty grid (or raise an error, depending on desired behavior)
    if blue_object is None:
        return np.array([])

    # Determine output grid size
    height, width = blue_object['dimensions']
    output_grid = np.ones((height, width), dtype=int)

    return output_grid
```
