# 39a8645d • 002 • example_3 • investigate_coder

---
```python
"""
Identify the largest connected component (contiguous block of pixels) of a single non-zero color, ignoring single isolated pixels. Extract a 3x3 grid representing the core shape, padding with 0s where the selected color is not present.
"""

import numpy as np

def get_largest_object(grid):
    """
    Finds the largest connected component of a single non-zero color, excluding single pixels.
    """
    visited = np.zeros_like(grid, dtype=bool)
    max_size = 0
    max_object_color = 0
    max_object_coords = []

    def dfs(row, col, color, coords):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return 0
        visited[row, col] = True
        coords.append((row, col))
        size = 1
        size += dfs(row + 1, col, color, coords)
        size += dfs(row - 1, col, color, coords)
        size += dfs(row, col + 1, color, coords)
        size += dfs(row, col - 1, color, coords)
        return size

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                coords = []
                size = dfs(r, c, grid[r, c], coords)
                if size > max_size and size > 1: # ignore isolated pixels
                  max_size = size
                  max_object_color = grid[r,c]
                  max_object_coords = coords
                elif size == max_size and size > 1: # there is only 1 prominent object.
                  pass

    return max_object_color, max_object_coords

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    # 1. Identify the Target Object
    target_color, target_coords = get_largest_object(input_grid)

    # 2. (Bounding Box not explicitly needed, as we work directly with coordinates)

    # 3. Extract 3x3 Centered Output
    output_grid = np.zeros((3, 3), dtype=int)

    if not target_coords: #handle empty
        return output_grid.tolist()

    # Find centroid of the object coordinates
    centroid_row = int(sum(coord[0] for coord in target_coords) / len(target_coords))
    centroid_col = int(sum(coord[1] for coord in target_coords) / len(target_coords))
    
    #translate coordinates
    for r in range(3):
        for c in range(3):
            check_row = centroid_row + (r-1)
            check_col = centroid_col + (c-1)
            if 0 <= check_row < input_grid.shape[0] and 0 <= check_col < input_grid.shape[1] and input_grid[check_row, check_col] == target_color:
              output_grid[r,c] = target_color


    return output_grid.tolist()
```
