# 760b3cac • 010 • refine_coder

---
```python
"""
Identifies distinct azure (8) and yellow (4) regions. The azure
region expands, primarily to the right, but is constrained by yellow regions
and tends to form a rectangular shape. Yellow regions remain unchanged.
"""

import numpy as np

def find_regions(grid, color):
    """Finds contiguous regions of a specific color."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = []

    def dfs(r, c, current_region):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_region.append((r, c))
        dfs(r + 1, c, current_region)
        dfs(r - 1, c, current_region)
        dfs(r, c + 1, current_region)
        dfs(r, c - 1, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                regions.append(current_region)
    return regions

def get_bounding_box(region):
    """Calculates the bounding box of a region."""
    min_r = min(r for r, c in region)
    max_r = max(r for r, c in region)
    min_c = min(c for r, c in region)
    max_c = max(c for r, c in region)
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find azure and yellow regions
    azure_regions = find_regions(input_grid, 8)
    yellow_regions = find_regions(input_grid, 4)

    # Expand azure regions
    for azure_region in azure_regions:
        # Get bounding box for rectangular expansion
        min_r, max_r, min_c, max_c = get_bounding_box(azure_region)

        # expand to the right, within bounding box
        for r in range(min_r, max_r + 1):
            for c in range(min_c, cols):  # iterate through to end of row
               if input_grid[r,c] == 0:
                  output_grid[r,c] = 8

        # expand the rectangle downward within bounding box.
        for r in range(min_r, rows):
            for c in range(min_c, max_c + 1):
               if input_grid[r,c] == 0:
                  output_grid[r,c] = 8

    return output_grid
```
