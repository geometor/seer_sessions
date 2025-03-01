# 7447852a • 004 • refine_coder

---
```python
"""
1.  **Identify Red Pixels:** Scan the input grid and identify all pixels that are red (color value 2).
2.  **Classify Red Pixels**: Determine if each red pixel is either *isolated* (not horizontally or vertically adjacent to any other red pixel) or a *region member* (part of a contiguous group of 3 or more red pixels, connected horizontally or vertically).
3.  **Transform Regions**: Change the color of red pixels that are *region members* to yellow (color value 4).
4. **Preserve other pixels**: Maintain original colors of all other colors as well as isolated red pixels.
"""

import numpy as np

def is_isolated(grid, x, y, color):
    """Checks if a pixel at (x, y) of a given color is isolated."""
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            if dx != 0 and dy != 0:
                continue #only check horizontal and vertical

            nx, ny = x + dx, y + dy
            if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] == color:
                return False
    return True

def find_regions(grid, color):
    visited = set()
    regions = []

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_region):
        if (x, y) in visited or not is_valid(x, y) or grid[x, y] != color:
            return
        visited.add((x, y))
        current_region.append((x, y))

        dfs(x + 1, y, current_region)
        dfs(x - 1, y, current_region)
        dfs(x, y + 1, current_region)
        dfs(x, y - 1, current_region)


    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if (x, y) not in visited and grid[x, y] == color:
                current_region = []
                dfs(x, y, current_region)
                if len(current_region) >= 3:
                   regions.append(current_region)

    return regions

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    red_regions = find_regions(input_grid, 2)
    
    #fill large red regions with yellow
    for region in red_regions:
        for x, y in region:
          output_grid[x,y] = 4
          
    return output_grid
```
