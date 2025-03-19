# 0dfd9992 • 002 • example_3 • investigate_coder

---
```python
"""
Identifies and removes specific contiguous regions of white (0) pixels from the input grid.
"""

import numpy as np

def get_contiguous_regions(grid, color):
    """
    Finds contiguous regions of a specific color in the grid.
    Uses Depth-First Search (DFS) to find connected components.
    """
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == color:
                regions.append(dfs(row, col))
    return regions

def transform(input_grid):
    """
    Transforms the input grid by removing specific white regions.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find all contiguous regions of white (0) pixels
    white_regions = get_contiguous_regions(input_grid, 0)

    # Remove the identified regions
    for region in white_regions:
        for row,col in region:
            output_grid[row,col] = input_grid[row,col]
       
    return output_grid
```
