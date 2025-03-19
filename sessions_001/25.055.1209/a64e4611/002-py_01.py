"""
Fills some of the azure regions in the input grid with green, leaving the white background and other azure regions unchanged.
"""

import numpy as np

def find_azure_regions(grid):
    """Finds contiguous regions of azure (8) pixels."""
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

def fill_region_with_bounds(grid, region, color):
    """Fills a region defined by its bounding box with the specified color."""
    if not region:
        return

    min_r = min(r for r, _ in region)
    max_r = max(r for r, _ in region)
    min_c = min(c for _, c in region)
    max_c = max(c for _, c in region)

    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            grid[r, c] = color

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find all azure regions
    azure_regions = find_azure_regions(input_grid)
    
    # determine which region to fill
    # must include some azure at a distance of 1 in all rows or columns
    fill_region = []
    for region in azure_regions:
        rows = set()
        cols = set()
        for r, c in region:
            rows.add(r)
            cols.add(c)
        
        # check distance condition
        all_rows_close = all(any(abs(r - test_r) <=1 for test_r,_ in region ) for r in range(input_grid.shape[0]))
        all_cols_close = all(any(abs(c - test_c) <=1 for _,test_c in region ) for c in range(input_grid.shape[1]))        
        if all_rows_close or all_cols_close:
          fill_region = region
          break

    # Fill the determined region in the output_grid with green (3)
    fill_region_with_bounds(output_grid, fill_region, 3)

    return output_grid