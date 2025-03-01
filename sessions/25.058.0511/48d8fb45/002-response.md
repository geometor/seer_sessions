# 48d8fb45 • 002 • example_1 • investigate_coder

---
```python
"""
Identify the largest connected region of blue (1) pixels within the input grid. 
Extract a subgrid from a section of the input grid, keeping only the blue (1) pixels and replacing everything else with white (0).
"""

import numpy as np

def find_largest_blue_region(grid):
    # helper function to use in find_blue_region
    def dfs(row, col, visited, region):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                (row, col) in visited or grid[row, col] != 1):
            return
        visited.add((row, col))
        region.append((row, col))
        dfs(row + 1, col, visited, region)
        dfs(row - 1, col, visited, region)
        dfs(row, col + 1, visited, region)
        dfs(row, col - 1, visited, region)

    visited = set()
    largest_region = []
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 1 and (row, col) not in visited:
                current_region = []
                dfs(row, col, visited, current_region)
                if len(current_region) > len(largest_region):
                    largest_region = current_region
    return largest_region
    
def get_bounding_box(region):
    min_row = min(r[0] for r in region)
    max_row = max(r[0] for r in region)
    min_col = min(r[1] for r in region)
    max_col = max(r[1] for r in region)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the largest connected region of blue pixels.
    largest_blue_region = find_largest_blue_region(input_grid)

    # get the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(largest_blue_region)
    
    # extract that region
    output_grid = np.zeros((max_row-min_row+1, max_col-min_col+1), dtype=int)
    
    for r, c in largest_blue_region:
      output_grid[r-min_row, c-min_col] = 1

    return output_grid
```
