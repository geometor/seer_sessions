```python
"""
1.  **Identify Regions:** Identify all contiguous regions of orange (7) pixels and red (2) pixels. A region consists of pixels of the same color connected horizontally or vertically.
2.  **Determine Adjacency:** For each orange region, check if it is adjacent to *any* red region. Adjacency is defined as sharing a horizontal or vertical border.
3.  **Transform Orange Regions:**
    *   If an orange region is adjacent to *any* red region, change all pixels in that orange region to green (3).
    *   If an orange region is *not* adjacent to any red region, change all pixels in that orange region to gray (5).
4.  **Preserve Red Regions:** Red (2) pixels remain unchanged.
5.  **Preserve Other Regions:** Other color pixels (e.g. Blue (1) in the third example) are unchanged.
"""

import numpy as np

def get_regions(grid, color):
    """
    Identifies contiguous regions of a specific color in the grid.
    NOTE: This implementation uses a manual flood-fill approach as a workaround because SciPy is unavailable.
    """
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_region):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_region.append((r, c))
        dfs(r + 1, c, current_region)
        dfs(r - 1, c, current_region)
        dfs(r, c + 1, current_region)
        dfs(r, c - 1, current_region)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                regions.append(np.array(current_region))  # Convert list of tuples to numpy array
    return regions

def is_adjacent(region, other_color_regions, grid):
    """
    Checks if a given region is adjacent to any region of another color.
    """
    for r, c in region:
        neighbors = []
        if r > 0:
            neighbors.append((r - 1, c))  # Up
        if r < grid.shape[0] - 1:
            neighbors.append((r + 1, c))  # Down
        if c > 0:
            neighbors.append((r, c - 1))  # Left
        if c < grid.shape[1] - 1:
            neighbors.append((r, c + 1))  # Right

        for neighbor_row, neighbor_col in neighbors:
            for other_region in other_color_regions:
                if (neighbor_row, neighbor_col) in map(tuple, other_region): # using map to make compatible with numpy
                    return True
    return False

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # 1. Identify Regions - using a custom implementation due to the scipy limitation
    orange_regions = get_regions(input_grid, 7)
    red_regions = get_regions(input_grid, 2)

    # 2 & 3. Transform Orange Regions based on Adjacency
    for orange_region in orange_regions:
        if is_adjacent(orange_region, red_regions, input_grid):
            for r, c in orange_region:
                output_grid[r, c] = 3  # Change to green
        else:
            for r, c in orange_region:
                output_grid[r, c] = 5  # Change to gray

    return output_grid
```