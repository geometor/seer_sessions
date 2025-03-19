"""
1.  **Identify Enclosed Regions:** Scan the input grid to find all contiguous regions of white (0) pixels that are *completely* enclosed by blue (1) pixels. A region is considered enclosed only if *all* of its constituent white pixels have neighboring blue pixels in all four cardinal directions (up, down, left, right).

2. **Identify Open Regions** Scan the input grid to find all contiguous regions of white (0) pixels that have at least one pixel in the group that does not have all blue pixels for neighbors in all for cardinal directions.

3.  **Fill Inner Regions:** Fill the enclosed white regions with orange (7).

4.  Leave the surrounding blue (1) pixels unchanged. Do not change the open white regions.
"""

import numpy as np
from collections import deque

def get_neighbors(grid, r, c):
    """Gets the valid neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def is_enclosed(grid, r, c):
    """Checks if a white pixel is completely enclosed by blue pixels."""
    for nr, nc in get_neighbors(grid, r, c):
        if grid[nr, nc] != 1:
            return False
    return True

def find_enclosed_regions(grid):
    """Finds contiguous regions of 0s surrounded by 1s."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = []

    def bfs(r, c, current_region):
        queue = deque([(r, c)])
        visited[r, c] = True
        all_enclosed = True

        while queue:
            cr, cc = queue.popleft()
            current_region.append((cr, cc))

            if not is_enclosed(grid, cr, cc):
                all_enclosed = False

            for nr, nc in get_neighbors(grid, cr, cc):
                if grid[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

        return all_enclosed

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0 and not visited[r, c]:
                current_region = []
                all_enclosed = bfs(r, c, current_region)
                if all_enclosed:
                    regions.append(current_region)
    return regions


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find enclosed regions
    enclosed_regions = find_enclosed_regions(input_grid)

    # Fill enclosed regions with orange (7)
    for region in enclosed_regions:
        for r, c in region:
            output_grid[r, c] = 7

    return output_grid