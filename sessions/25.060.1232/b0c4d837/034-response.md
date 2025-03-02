# b0c4d837 • 034 • example_6 • investigate_coder

---
```python
"""
1.  **Identify the Target Region:** Locate the contiguous region of azure (8) pixels within the input grid. This region is enclosed or surrounded by gray (5) pixels that form an upside-down "U" shape.
2.  **Extract the Bounding Box:** Determine minimum bounding box of the azure region.
3.  **Output the Azure Region:** Create new grid using only the bounding box of the azure pixels.
"""

import numpy as np

def find_contiguous_region(grid, color_value):
    """Finds the coordinates of a contiguous region of a given color."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    region = []

    def dfs(row, col):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color_value
        ):
            return
        visited[row, col] = True
        region.append((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color_value and not visited[row, col]:
                dfs(row, col)
                return region  # Return after finding the first region

    return region  # in case no region of the specified color is found

def bounding_box(region):
    """Calculates the bounding box of a set of coordinates."""
    if not region:
        return None
    min_row = min(r[0] for r in region)
    max_row = max(r[0] for r in region)
    min_col = min(r[1] for r in region)
    max_col = max(r[1] for r in region)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Find the contiguous region of azure (8) pixels.
    azure_region = find_contiguous_region(input_grid, 8)

    # Calculate the bounding box of the azure region.
    bbox = bounding_box(azure_region)

    # Create the output grid based on the bounding box.
    if bbox:
        (min_row, min_col), (max_row, max_col) = bbox
        output_grid = np.zeros((max_row - min_row + 1, max_col - min_col +1), dtype=int)
        for r, c in azure_region:
            output_grid[r-min_row,c-min_col] = 8
    else:
        output_grid = np.zeros_like(input_grid) # should not happen

    return output_grid
```
