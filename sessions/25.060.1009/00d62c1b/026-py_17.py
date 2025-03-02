"""
1.  Identify Green Regions: Find all contiguous regions of green (3) pixels in the input grid.
2.  Highlight All Green: For each green region, change *all* the green colored pixels within that region to yellow (4).
"""

import numpy as np

def find_contiguous_regions(grid, color):
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_region):
        if not is_valid(x, y) or visited[x, y] or grid[x, y] != color:
            return
        visited[x, y] = True
        current_region.append((x, y))
        dfs(x + 1, y, current_region)
        dfs(x - 1, y, current_region)
        dfs(x, y + 1, current_region)
        dfs(x, y - 1, current_region)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == color and not visited[x, y]:
                current_region = []
                dfs(x, y, current_region)
                regions.append(current_region)
    return regions

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find contiguous regions of green (3) pixels
    green_regions = find_contiguous_regions(input_grid, 3)

    # Iterate through each green region and change all green pixels to yellow
    for region in green_regions:
        for x, y in region:
            output_grid[x, y] = 4

    return output_grid