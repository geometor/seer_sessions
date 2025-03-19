# e509e548 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Connected Regions:** Find all contiguous regions of green (3) pixels in the input grid. Contiguous means connected orthogonally (up, down, left, or right).

2.  **Recolor Regions:** For each identified green region:
    *   If the region is at the top left of the image (the leftmost pixel in the region has x and y coordinates that are lesser or equal to all pixels), change all its pixels to blue (1).
    *   If the region is at the bottom left of the image, change all its pixels to red (2).
    *   If the region is at the top right of the image, change its pixels to magenta(6).
    *    All white (0) pixels remain unchanged.
"""

import numpy as np

def find_connected_regions(grid, color):
    # Find all connected regions of a specific color in the grid
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        # Depth-first search to find connected components
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def get_region_position(region):
    # simple method to determine position (top-left, bottom-left, top-right)
    min_row = min(r[0] for r in region)
    #max_row = max(r[0] for r in region)
    min_col = min(r[1] for r in region)
    max_col = max(r[1] for r in region)

    return min_row, min_col, max_col

def transform(input_grid):
    # Initialize output grid with the same dimensions and background color
    output_grid = np.zeros_like(input_grid)

    # Find connected regions of green (color 3)
    green_regions = find_connected_regions(input_grid, 3)

    # Recolor each region based on its position
    for region in green_regions:
        min_row, min_col, max_col = get_region_position(region)

        if min_row == 0 and min_col == 0 :  #top-left
            new_color = 1
        elif min_row >= 6 and min_col == 0: # bottom-left
              new_color = 2
        elif min_row == 0 and max_col > 0:   # top right
              new_color = 6
        else:
            new_color = 0

        for row, col in region:
            output_grid[row, col] = new_color


    return output_grid
```
