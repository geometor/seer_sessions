# f8ff0b80 • 006 • example_2 • investigate_coder

---
```python
"""
1. **Identify Distinct Regions:** Examine the input grid and identify all contiguous regions of non-zero pixels. Each region is defined by pixels of the same color that are adjacent (horizontally or vertically, not diagonally).

2.  **Extract Representative Colors:** For each identified region, extract its color value. Since all pixels within a region have the same color, any pixel from the region can provide this value.

3. **Order Colors:** Arrange the color values as follows: Blue (1) first, Orange(7) second and Red(2) third.

4.  **Construct Output:** Create a 3x1 output grid where each cell corresponds to the extracted color values in that order.
"""

import numpy as np

def find_regions(grid):
    """
    Finds distinct regions in a grid.
    """
    regions = {}
    visited = set()

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, color):
        if (x, y) in visited or not is_valid(x, y) or grid[x, y] != color:
            return []

        visited.add((x, y))
        region_pixels = [(x, y)]

        # Explore adjacent pixels (up, down, left, right)
        region_pixels.extend(dfs(x + 1, y, color))
        region_pixels.extend(dfs(x - 1, y, color))
        region_pixels.extend(dfs(x, y + 1, color))
        region_pixels.extend(dfs(x, y - 1, color))

        return region_pixels

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if (x, y) not in visited and grid[x, y] != 0:
                color = grid[x, y]
                region_pixels = dfs(x, y, color)
                if color not in regions:
                  regions[color] = region_pixels

    return regions
def transform(input_grid):
    """
    Transforms the input grid to the output grid based on identified regions and colors.
    """
    # Find distinct regions in the input grid
    regions = find_regions(np.array(input_grid))

    # Extract the color values from the identified regions
    colors = list(regions.keys())
    
    # Sort color values: blue (1), orange (7), and red (2)
    color_order = {
        1: 1,
        7: 2,
        2: 3
    }

    
    ordered_colors = sorted(colors, key=lambda x: color_order.get(x, float('inf')))


    # Construct the output grid (3x1)
    output_grid = np.array(ordered_colors).reshape(3, 1)

    return output_grid.tolist()
```
