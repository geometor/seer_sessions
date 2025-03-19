# a64e4611 • 005 • refine_coder

---
```python
"""
1. **Find Azure Regions:** Examine the input grid and identify all contiguous regions of azure (8) pixels. A contiguous region is a group of azure pixels where each pixel is directly adjacent (up, down, left, or right) to at least one other pixel in the region.

2. **Calculate Bounding Boxes:** For each identified azure region, determine its bounding box. The bounding box is the smallest rectangle that completely encloses the region, defined by (min_row, min_col, max_row, max_col).

3. **Determine Fill:**
    *   If any azure region's bounding box has the same dimensions as the entire grid, change all grid cells to green (3).
    *   Otherwise, iterate through each azure region. For each region, fill the area within its bounding box in the output grid with green (3), leaving other areas unchanged.
"""

import numpy as np

def find_azure_regions(grid):
    """Finds contiguous regions of azure (8) pixels."""
    grid = np.array(grid)
    azure_regions = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_region):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != 8:
            return
        visited[r, c] = True
        current_region.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, current_region)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 8 and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                azure_regions.append(current_region)
    return azure_regions

def calculate_bounds(region):
    """Calculates the bounding box of a region."""
    if not region:
        return None
    min_r = min(r for r, _ in region)
    max_r = max(r for r, _ in region)
    min_c = min(c for _, c in region)
    max_c = max(c for _, c in region)
    return (min_r, min_c, max_r, max_c)

def fill_region(grid, bounds, color):
    """Fills a region defined by its bounding box with the specified color."""
    if bounds is None:
        return
    min_r, min_c, max_r, max_c = bounds
    grid[min_r:max_r+1, min_c:max_c+1] = color

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)

    # Find all azure regions
    azure_regions = find_azure_regions(input_grid)
    
    # Check if any region's bounding box matches the grid size
    grid_bounds = (0, 0, output_grid.shape[0] - 1, output_grid.shape[1] - 1)
    for region in azure_regions:
        bounds = calculate_bounds(region)
        if bounds == grid_bounds:
            # Fill the entire grid with green
            fill_region(output_grid, grid_bounds, 3)
            return output_grid

    # Fill each region based on its bounding box
    for region in azure_regions:
        bounds = calculate_bounds(region)
        fill_region(output_grid, bounds, 3)

    return output_grid
```
