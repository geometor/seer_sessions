# a740d043 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule extracts non-blue regions from the input grid and combines them into the output grid.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous non-blue regions (objects) in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 1:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by extracting non-blue regions.
    """
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)
    
    # Find objects (non-blue regions)
    objects = find_objects(input_grid)

    # If no objects are found, return an empty grid (or handle as needed)
    if not objects:
        return []

    # Find the bounding box encompassing all objects
    min_row = min(min(obj[0] for obj in object_) for object_ in objects)
    max_row = max(max(obj[0] for obj in object_) for object_ in objects)
    min_col = min(min(obj[1] for obj in object_) for object_ in objects)
    max_col = max(max(obj[1] for obj in object_) for object_ in objects)
    
    # Create the output grid based on the bounding box
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

     # Fill the output grid with values from the objects
    for object_ in objects:
        for r, c in object_:
             output_grid[r - min_row, c - min_col] = input_grid[r,c]

    return output_grid.tolist()
```
