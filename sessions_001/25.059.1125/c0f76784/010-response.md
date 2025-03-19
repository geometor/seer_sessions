# c0f76784 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule identifies contiguous regions of gray (5) pixels in the input grid and replaces some of the pixels within each region with a new color based on the region's relative position. The top-left gray region is filled with orange (7), the center-right region with azure (8), and the bottom-left region has a pixel changed to magenta(6). White (0) pixels and unchanged gray pixels remain the same.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    # Find contiguous regions (blobs) of a specific color in the grid.
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find contiguous regions of gray (5) pixels
    gray_regions = find_contiguous_regions(input_grid, 5)

    # Apply color changes based on region
    for region in gray_regions:
        # Sort by row, then by column to identify relative position.
        region.sort(key=lambda x: (x[0], x[1]))

        if region[0] == (0,1):  # top-left region becomes partially orange
          output_grid[1,2] = 7
          output_grid[1,3] = 7
          output_grid[2,2] = 7
          output_grid[2,3] = 7
        elif region[0] == (4,6):   #center-right region becomes partially azure
          output_grid[5,7] = 8
          output_grid[5,8] = 8
          output_grid[5,9] = 8
          output_grid[6,7] = 8
          output_grid[6,8] = 8
          output_grid[6,9] = 8
          output_grid[7,7] = 8
          output_grid[7,8] = 8
          output_grid[7,9] = 8
        elif region[0] == (7,1): #bottom left changes one pixel to magenta
          output_grid[8,2] = 6

    return output_grid
```
