# 5117e062 • 014 • refine_coder

---
```python
"""
1.  **Identify Green Objects:** Locate all distinct contiguous regions (objects) of green pixels within the input grid.
2.  **Extract and Position:** Extract each identified green object and move it to the top-left corner of the output grid, *without changing the size or orientation*.  If there are no green objects, return a blank grid. If the green object takes up more than the top-left corner, keep it in place.
"""

import numpy as np

def find_objects(grid, color):
    """Finds all distinct objects of a given color."""
    visited = set()
    objects = []

    def dfs(row, col):
        """Depth-first search to find contiguous regions."""
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []
        visited.add((row, col))
        coords = [(row, col)]
        coords.extend(dfs(row + 1, col))
        coords.extend(dfs(row - 1, col))
        coords.extend(dfs(row, col + 1))
        coords.extend(dfs(row, col - 1))
        return coords

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited and grid[row, col] == color:
                object_coords = dfs(row, col)
                objects.append(object_coords)
    return objects

def bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    if not coords:
        return 0, 0, 0, 0
    rows = [r for r, _ in coords]
    cols = [c for _, c in coords]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find all green objects.
    green_objects = find_objects(input_grid, 3)

    # If no green objects, return a 3x3 zero array.
    if not green_objects:
        return np.zeros((3, 3), dtype=int)

    # Get the bounding box of the *first* green object (as per the rule).
    min_row, max_row, min_col, max_col = bounding_box(green_objects[0])
    
    # check if the object is already taking the top-left space
    if min_row == 0 and min_col == 0:
        output_grid = input_grid.copy()
    else:
        # create output of the same dimension
        output_grid = np.zeros_like(input_grid)

        # Extract the object.
        object_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

        # Place object in top-left
        output_grid[:object_grid.shape[0], :object_grid.shape[1]] = object_grid
    
    return output_grid
```
