# 868de0fa • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Regions:** Scan the input grid to find all contiguous regions of white (0) pixels that are completely enclosed by blue (1) pixels. These form closed shapes.

2.  **Fill Inner Regions (Alternating):** Fill those white regions with two new colors following a pattern:
      *   Fill the inner most regions with red (2)
      *   Fill outer most regions with orange (7)

3.  Leave the surrounding blue (1) pixels, and the open white (0) pixel (not surrounded by 1's) unchanged.
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

def find_regions(grid):
    """Finds contiguous regions of 0s surrounded by 1s."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = []

    def bfs(r, c, current_region):
        queue = deque([(r, c)])
        visited[r, c] = True
        is_enclosed = True

        while queue:
            cr, cc = queue.popleft()
            current_region.append((cr, cc))

            for nr, nc in get_neighbors(grid, cr, cc):
                if grid[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))
                elif grid[nr, nc] != 0 and grid[nr, nc] != 1: # Added: Check for invalid surrounding
                    is_enclosed = False
                elif grid[nr, nc] == 0:
                    continue # already in queue or visited

                #check that the border is only color 1
                elif grid[nr, nc] != 1:
                     is_enclosed = False

        return is_enclosed

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0 and not visited[r, c]:
                current_region = []
                is_enclosed = bfs(r, c, current_region)
                if is_enclosed:
                    regions.append(current_region)

    return regions

def fill_regions(output_grid, regions):
    """ Fills identified regions with orange (7) or red (2).
        This simple version assumes non-overlapping and order based on index in list
    """
    for i, region in enumerate(regions):

        fill_color = 7 if (i % 2 == 0) else 2

        for r, c in region:
             output_grid[r,c] = fill_color

    return output_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    #find regions
    regions = find_regions(input_grid)
    # change output pixels: fill regions with orange or red
    output_grid = fill_regions(output_grid, regions)

    return output_grid
```
