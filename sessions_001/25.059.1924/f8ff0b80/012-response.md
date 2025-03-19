# f8ff0b80 • 012 • example_3 • investigate_coder

---
```python
"""
Identifies colored regions (excluding white/0) in the input grid, sorts these regions by their color values in descending order, and outputs a vertical stack of the color values.
"""

import numpy as np

def find_regions(grid):
    """
    Finds contiguous regions of the same color in a grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, color, region_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        region_pixels.append((row, col))
        dfs(row + 1, col, color, region_pixels)
        dfs(row - 1, col, color, region_pixels)
        dfs(row, col + 1, color, region_pixels)
        dfs(row, col - 1, color, region_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                region_pixels = []
                dfs(row, col, grid[row, col], region_pixels)
                regions.append({'value': grid[row, col], 'pixels': region_pixels})
    return regions

def transform(input_grid):
    # Find regions in the input grid
    regions = find_regions(np.array(input_grid))

    # Sort regions by color value in descending order
    sorted_regions = sorted(regions, key=lambda x: x['value'], reverse=True)

    # Create output grid
    output_grid = []
    for region in sorted_regions:
      output_grid.append([region['value']])

    return output_grid
```
