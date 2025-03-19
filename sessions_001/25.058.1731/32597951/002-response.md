# 32597951 • 002 • example_3 • investigate_coder

---
```python
"""
Identifies a contiguous region of azure (8) colored pixels within a grid.
Replaces the inner 3x3 area of the azure region with green (3).
The rest of the grid remains unchanged.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    # Find contiguous regions of a specific color in the grid.
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
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

def get_object_bounds(region):
     # get the bounding box
    min_row = min(r[0] for r in region)
    max_row = max(r[0] for r in region)
    min_col = min(r[1] for r in region)
    max_col = max(r[1] for r in region)
    return min_row, max_row, min_col, max_col
    

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find contiguous regions of azure color.
    azure_regions = find_contiguous_regions(output_grid, 8)
    
    # Iterate through each azure region.
    for azure_region in azure_regions:
        #Compute the bounding box for the region.
        min_row, max_row, min_col, max_col = get_object_bounds(azure_region)
        
        # Check if region is large enough
        if max_row - min_row >= 2 and max_col - min_col >= 2:
            # inner 3x3 region
            for r in range(min_row + 1, max_row):
                for c in range(min_col+1, max_col):
                     output_grid[r,c] = 3

    return output_grid
```
