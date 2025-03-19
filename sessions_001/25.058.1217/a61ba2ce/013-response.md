# a61ba2ce • 013 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous regions (objects) of non-zero pixels in the input grid.
2. **Determine Significant Colors:** The output grid will contain a subset of colors in the input
    grid. Significant colors appear to be, in order of priority, are:
        Example 1: 1, 8, 4, 2
        Example 2: 1, 8, 4
        Example 3: 7
3. **Create Combined Bounding Box:** For each significant colors, find all pixels with that color
    in the input grid. Create one combined bounding box for all pixels of all significant colors.
4.  **Extract Sub-grid:** Extract the rectangular region defined by the combined bounding box from the input grid.
5.  **Output:** The extracted sub-grid is the output. If no significant colors found - return an empty grid? (need clarification on edge case)
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                if obj_pixels:
                    objects.append({'color': grid[row, col], 'pixels': obj_pixels})
    return objects

def get_bounding_box(pixels):
    """Calculates the bounding box for a set of pixels."""
    if not pixels:
        return None
    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # 1. Identify Objects
    # objects = find_objects(input_grid)  # Not strictly needed, we just need the pixels

    # 2. Determine Significant Colors (and their priority)
    significant_colors = [1, 8, 4, 2, 7]  # Combined list, order matters

    # 3. Create Combined Bounding Box
    all_significant_pixels = []
    for color in significant_colors:
        for row in range(input_grid.shape[0]):
            for col in range(input_grid.shape[1]):
                if input_grid[row, col] == color:
                    all_significant_pixels.append((row, col))

    bounding_box = get_bounding_box(all_significant_pixels)

    # 4. Extract Sub-grid (Handle the case where no significant colors are found)
    if bounding_box is None:
        return np.array([[]])  # Return an empty grid
    
    (min_row, min_col), (max_row, max_col) = bounding_box
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    # 5. Output
    return output_grid
```
