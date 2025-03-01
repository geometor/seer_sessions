# 72322fa7 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule replicates non-white pixel groups (yellow and azure) across both horizontal and vertical axes.
Existing objects are mirrored to the opposite half of the grid, both horizontally and vertically.
"""

import numpy as np

def find_objects(grid):
    """Finds non-white objects in the grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, obj_id, color):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return []

        visited.add((r, c))
        object_pixels = [(r, c)]

        # Check adjacent pixels (horizontal and vertical)
        neighbors = [(r, c + 1), (r, c - 1)]  # Simplified to horizontal for this specific pattern
        for nr, nc in neighbors:
             object_pixels.extend(dfs(nr, nc, obj_id, color))

        return object_pixels

    obj_id_counter = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj_pixels = dfs(r, c, obj_id_counter, grid[r, c])
                if obj_pixels:
                    objects.append({
                        "id": obj_id_counter,
                        "color": grid[r, c],
                        "pixels": obj_pixels
                    })
                    obj_id_counter += 1

    return objects

def replicate_object(grid, obj, output_grid):
    """Replicates an object horizontally and vertically."""
    rows, cols = grid.shape
    for r, c in obj["pixels"]:
        # Original object
        output_grid[r, c] = obj["color"]

        # Horizontal reflection
        mirrored_c = cols - 1 - c
        output_grid[r, mirrored_c] = obj["color"]

        # Vertical reflection
        mirrored_r = rows - 1- r
        output_grid[mirrored_r,c] = obj["color"]

        # Both
        output_grid[mirrored_r, mirrored_c] = obj["color"]

    return output_grid

def transform(input_grid):
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find non-white objects in the input grid
    objects = find_objects(input_grid)
    # Replicate each object in the other halves
    for obj in objects:
      output_grid = replicate_object(input_grid, obj, output_grid)

    return output_grid
```
