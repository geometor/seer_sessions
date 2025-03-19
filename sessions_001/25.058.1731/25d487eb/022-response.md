# 25d487eb • 022 • refine_coder

---
```python
"""
1.  **Identify Green Regions:** Find all contiguous regions of green pixels.
2.  **Identify Red Pixels within Green Regions:** Find all red pixels that are located *inside* a green region.
3.  **Conditional Extension:** Iterate through each red pixel within the green area. Extend the red color upwards, overwriting only background pixels.
"""

import numpy as np

def find_green_regions(grid):
    """Finds contiguous regions of green pixels."""
    green_regions = []
    visited = np.zeros_like(grid, dtype=bool)
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 3 and not visited[r, c]:
                region = []
                stack = [(r, c)]
                visited[r, c] = True
                while stack:
                    row, col = stack.pop()
                    region.append((row, col))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and grid[nr, nc] == 3 and not visited[nr, nc]:
                            stack.append((nr, nc))
                            visited[nr, nc] = True
                green_regions.append(region)
    return green_regions

def is_inside_green(row, col, green_regions):
    """Checks if a given pixel is within any of the green regions."""
    for region in green_regions:
        if (row, col) in region:
            return True
    return False
    
def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find green regions
    green_regions = find_green_regions(input_grid)

    # Iterate through each pixel to find red pixels inside green regions and extend upwards
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
        if input_grid[r,c] == 2 and is_inside_green(r, c, green_regions):
          # extend red color upwards
          for ur in range(r -1, -1, -1):
            if output_grid[ur,c] == 0:
               output_grid[ur,c] = 2
            else:
               break
    return output_grid
```
