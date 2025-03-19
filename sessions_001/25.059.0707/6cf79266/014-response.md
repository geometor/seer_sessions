# 6cf79266 • 014 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Target Regions:** Scan the input grid for white pixels (0).

2.  **Conditional Insertion:** For selected white areas, check its orange surrounding, if specific configuarations exist.
    Insert 3x1 blue (1) blocks at the bottom of the left, middle and right white areas.

3.  **Preserve Other Pixels:** All other pixels in the grid (orange (7)) remain unchanged.
"""

import numpy as np

def find_white_regions(grid):
    """Find contiguous white regions in the grid."""
    white_regions = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_region):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != 0
        ):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 0 and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                white_regions.append(current_region)
    return white_regions

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    white_regions = find_white_regions(input_grid)

    # Iterate through identified white regions
    for region in white_regions:
        #find bottom row for region
        if len(region) > 0:

          bottom_row = max(region, key=lambda item: item[0])[0]
          region_cols = [col for row, col in region if row == bottom_row]

          #insert at the bottom, center of each region.
          if len(region_cols) > 0:
            insert_col = region_cols[len(region_cols) // 2]

            # Check to see if there is room for 3x1 block.
            if bottom_row + 2 < input_grid.shape[0]:
              output_grid[bottom_row, insert_col] = 1
              output_grid[bottom_row + 1, insert_col] = 1
              output_grid[bottom_row + 2, insert_col] = 1

    return output_grid
```
