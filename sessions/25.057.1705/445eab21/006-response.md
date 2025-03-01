# 445eab21 • 006 • refine_coder

---
```python
"""
1.  **Find Azure Object:** Examine the input grid to locate any contiguous regions of azure (color code 8) pixels. These regions constitute "objects."
2.  **Bounding Box:** If an azure object is found, determine its bounding box. The bounding box is defined by the minimum and maximum row and column indices of the azure pixels.
3.  **Direct Extraction:** Create a new grid whose dimensions match the height and width of the azure object's bounding box. Copy the pixel values from the input grid that fall *within* the bounding box to the corresponding locations in the output grid.
4.  **No Azure Case:** If no azure object is found, the output is an empty grid (zero dimensions).
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of the same color in a grid."""
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
            if not visited[row, col] and grid[row,col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def get_bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Find all objects
    objects = find_objects(input_grid)

    # Find azure object
    azure_object = None
    for obj in objects:
        if input_grid[obj[0]] == 8:
            azure_object = obj
            break

    # Handle no azure case
    if azure_object is None:
        return np.zeros((0, 0), dtype=int)

    # Get bounding box for azure object
    top_left, bottom_right = get_bounding_box(azure_object)
    
    # compute height, width of azure object bounding box
    azure_height = bottom_right[0] - top_left[0] + 1
    azure_width = bottom_right[1] - top_left[1] + 1

    # Initialize output (start by assuming same size of azure bounding box)
    output_grid = np.zeros((azure_height, azure_width), dtype=int)

    # Direct Extraction
    for row in range(azure_height):
        for col in range(azure_width):
            output_grid[row, col] = input_grid[top_left[0] + row, top_left[1] + col]
    
    return output_grid
```

