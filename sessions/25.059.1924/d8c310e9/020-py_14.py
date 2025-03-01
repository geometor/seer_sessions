"""
1. Identify Colored Regions: Find all contiguous regions of non-white pixels in the input grid. Consider each isolated non-white pixel as its own region.
2. Duplicate Regions to the Right: For each identified region, duplicate every pixel immediately to the right of the original position. The copied region should be the exact same as the original region.
"""

import numpy as np

def find_colored_regions(grid):
    """
    Finds all contiguous colored regions (including single pixels).
    Returns a list of regions, where each region is a list of (row, col, color) tuples.
    """
    rows, cols = grid.shape
    regions = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_region):
        visited.add((r, c))
        current_region.append((r, c, grid[r, c]))

        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if is_valid(nr, nc) and (nr, nc) not in visited and grid[nr, nc] == grid[r, c]:
                dfs(nr, nc, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_region = []
                dfs(r, c, current_region)
                regions.append(current_region)

    return regions

def transform(input_grid):
    """
    Transforms the input grid by identifying colored regions and duplicating them to the right.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find colored regions
    regions = find_colored_regions(input_grid)

    # Iterate through each region
    for region in regions:
        # Duplicate the region to the right
        for r, c, color in region:
            new_col = c + 1  # Calculate new column index (immediately to the right)
            if new_col < cols: # make sure not outside grid
                output_grid[r, new_col] = color

    return output_grid