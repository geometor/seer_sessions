"""
Identifies distinct azure (8) and yellow (4) regions. The azure
regions expand in all directions to fill available space while maintaining a
rectangular shape, constrained by yellow regions. Yellow regions remain unchanged.
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

def expand_to_rectangle(grid, region):
    """Expands the region to the largest possible rectangle."""
    min_r, max_r, min_c, max_c = get_bounding_box(region)
    rows, cols = grid.shape

    # Expand up
    while min_r > 0 and all(grid[min_r - 1, c] in [0, 8] for c in range(min_c, max_c + 1)):
        min_r -= 1

    # Expand down
    while max_r < rows - 1 and all(grid[max_r + 1, c] in [0, 8] for c in range(min_c, max_c + 1)):
        max_r += 1

    # Expand left
    while min_c > 0 and all(grid[r, min_c - 1] in [0, 8] for r in range(min_r, max_r + 1)):
        min_c -= 1

    # Expand right
    while max_c < cols - 1 and all(grid[r, max_c + 1] in [0, 8] for r in range(min_r, max_r + 1)):
        max_c += 1

    return min_r, max_r, min_c, max_c

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find azure and yellow regions
    azure_regions = find_regions(input_grid, 8)
    yellow_regions = find_regions(input_grid, 4)

    # Expand azure regions
    for azure_region in azure_regions:
        min_r, max_r, min_c, max_c = expand_to_rectangle(input_grid, azure_region)

        # Fill the expanded rectangle with azure
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                output_grid[r, c] = 8

    return output_grid