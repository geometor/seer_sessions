"""
Fills the top-most, left-most azure region in the input grid with green, leaving the white background and other azure regions unchanged. If the entire grid is azure, it fills the entire grid with green.
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

def fill_region(grid, region, color):
    """Fills a region with the specified color."""
    for r, c in region:
        grid[r, c] = color

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find all azure regions
    azure_regions = find_azure_regions(input_grid)

    # Handle all-azure case
    if all(input_grid.flatten() == 8):
        fill_region(output_grid, [(r, c) for r in range(output_grid.shape[0]) for c in range(output_grid.shape[1])], 3)
        return output_grid

    # Select top-left region
    if azure_regions:
        fill_region_ = sorted(azure_regions, key=lambda region: (min(r for r, _ in region), min(c for _, c in region)))[0]

      # Fill the determined region in the output_grid with green (3)
        fill_region(output_grid, fill_region_, 3)

    return output_grid