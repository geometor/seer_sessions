# 868de0fa • 020 • refine_coder

---
```python
"""
1.  **Identify Regions:** Examine the grid and identify all contiguous regions of white (0) pixels.
2.  **Determine Fill Condition:**
    *   If a white region is *completely* enclosed by blue (1) pixels (all neighboring pixels in the four cardinal directions are blue), it should be filled.
    *   If *no* white regions are completely enclosed by blue pixels, fill *all* white regions.
3.  **Fill Regions:** Change the color of the pixels in the identified white regions to orange (7).
4. **Preserve Other Pixels:** All non-white pixels (in the examples, only blue (1) pixels have been observed), should remain unchanged.
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

def find_white_regions(grid):
    """Finds all contiguous regions of white (0) pixels."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = []

    def bfs(r, c, current_region):
        queue = deque([(r, c)])
        visited[r, c] = True

        while queue:
            cr, cc = queue.popleft()
            current_region.append((cr, cc))

            for nr, nc in get_neighbors(grid, cr, cc):
                if grid[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0 and not visited[r, c]:
                current_region = []
                bfs(r, c, current_region)
                regions.append(current_region)
    return regions

def find_enclosed_regions(grid, white_regions):
    """Finds white regions that are fully enclosed"""
    enclosed_regions = []
    for region in white_regions:
        all_enclosed = True
        for r, c in region:
            if not is_enclosed(grid, r, c):
                all_enclosed = False
                break
        if all_enclosed:
            enclosed_regions.append(region)
    return enclosed_regions
            

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all white regions
    white_regions = find_white_regions(input_grid)

    # Find enclosed white regions
    enclosed_regions = find_enclosed_regions(input_grid, white_regions)
    
    # Determine which regions to fill
    if enclosed_regions:
        regions_to_fill = enclosed_regions
    else:
        regions_to_fill = white_regions

    # Fill regions with orange (7)
    for region in regions_to_fill:
        for r, c in region:
            output_grid[r, c] = 7

    return output_grid
```
