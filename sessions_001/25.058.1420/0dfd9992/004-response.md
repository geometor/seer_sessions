# 0dfd9992 • 004 • refine_coder

---
```python
"""
Removes white (0) regions from the input grid based on whether they are enclosed by other colors.
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

def is_enclosed(grid, region):
    """
    Checks if a region is enclosed by non-white pixels.
    """
    rows, cols = grid.shape
    for r, c in region:
        # Check neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr, nc] != 0:
                        continue  # Neighbor is not white, continue checking
                else: #if any neighbor goes out of bounds, the region is not enclosed
                    return False
    return True #if region is not enclosed, return False
  

def transform(input_grid):
    """
    Transforms the input grid by removing enclosed white regions.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find all contiguous regions of white (0) pixels
    white_regions = get_contiguous_regions(input_grid, 0)

    # Remove the enclosed regions
    for region in white_regions:
        if is_enclosed(input_grid, region):
            for row, col in region:
                output_grid[row, col] = 1  # Fill with blue (or any non-white color)

    return output_grid
```
