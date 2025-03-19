# 7447852a • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Red Regions:** Scan the input grid and identify all contiguous regions of red (2) pixels. A region is defined as a group of horizontally or vertically adjacent pixels of the same color.
2.  **Filter large regions:** Keep regions of red pixels that contains 3 or more pixels.
3.  **Fill with Yellow:** For each region identified above, change the color of those pixels to yellow (4) in the output grid.
4.  **Preserve Other Pixels:** All other pixels in the input grid that are not part of a large red region retain their original color in the output grid.
"""

import numpy as np

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
    
    # find all red regions
    red_regions = find_regions(input_grid, 2)

    #fill large red regions with yellow
    for region in red_regions:
       for x, y in region:
          output_grid[x,y] = 4

    return output_grid
```
