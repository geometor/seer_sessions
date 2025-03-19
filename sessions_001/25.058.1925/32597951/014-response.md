# 32597951 • 014 • refine_coder

---
```python
"""
The transformation identifies contiguous regions of azure (8) pixels. Within each region, the 'center' azure pixel is changed to green (3). 
The center is defined as the pixel in the region with the smallest row and, if there's a tie, the smallest column.
"""

import numpy as np

def find_azure_regions(grid):
    """
    Finds all contiguous regions of azure (8) pixels.
    Returns a list of sets, where each set contains the (row, col) coordinates of a region.
    """
    rows, cols = grid.shape
    visited = set()
    regions = []

    def dfs(row, col, current_region):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != 8:
            return
        visited.add((row, col))
        current_region.add((row, col))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(row + dr, col + dc, current_region)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == 8 and (row, col) not in visited:
                current_region = set()
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def find_center_pixel(region):
    """
    Finds the "center" pixel of a region.  The center is the pixel with the smallest
    row and then the smallest column, if rows are tied.
    """
    min_row = float('inf')
    min_col = float('inf')
    for row, col in region:
      if row < min_row:
        min_row = row
        min_col = col
      elif row == min_row:
        min_col = min(min_col, col)
    return min_row, min_col

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find all contiguous regions of azure pixels
    azure_regions = find_azure_regions(input_grid)

    # For each region, find the "center" pixel and change it to green
    for region in azure_regions:
        center_row, center_col = find_center_pixel(region)
        output_grid[center_row, center_col] = 3

    return output_grid
```
