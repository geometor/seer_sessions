# 484b58aa • 006 • refine_coder

---
```python
"""
Identifies the contiguous region of non-black (non-zero) pixels within the input grid,
calculates the dimensions of the bounding box that encloses the region,
creates a new output grid with those dimensions,
and copies the pixels of the identified region to the output grid.
"""

import numpy as np

def get_objects(grid):
    """Identifies contiguous objects of the same color."""
    objects = []
    visited = set()

    def dfs(row, col, color, obj_coords):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or (row, col) in visited
            or grid[row, col] != color
        ):
            return

        visited.add((row, col))
        obj_coords.append((row, col))
        # Explore adjacent cells
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                if obj_coords:
                    objects.append(
                        {
                            "color": color,
                            "coordinates": obj_coords,
                            "shape": "contiguous",
                        } # Simplified for now
                    )
    return objects

def transform(input_grid):
    # Find the non-black object
    input_objects = get_objects(input_grid)
    non_black_object = None
    for obj in input_objects:
        if obj["color"] != 0:
            non_black_object = obj
            break

    if non_black_object is None:
        return np.array([]) # Return empty if there's no object

    # Determine output dimensions
    coords = non_black_object["coordinates"]
    rows = [c[0] for c in coords]
    cols = [c[1] for c in coords]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Create output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy object
    for row, col in coords:
        output_grid[row - min_row, col - min_col] = input_grid[row, col]

    return output_grid
```
