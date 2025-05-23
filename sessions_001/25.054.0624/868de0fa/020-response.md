# 868de0fa • 020 • example_4 • investigate_coder

---
```python
"""
1.  **Identify Regions:** Locate all contiguous regions of blue (1) pixels in the input grid.
2.  **Bottom transformation:** The bottom-most blue region is selected. Within this select region replace the blue color with orange except the border.
3.  **Center transformation:** Within the central large blue region in the top, a subregion, which is a rectangle of 2x2 and colored with red.
4. **Copy Unchanged:** All pixels that are not part of the identified blue regions (i.e., the white pixels) are copied unchanged from the input to the output grid.
"""

import numpy as np

def find_regions(grid, color):
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color and not visited[i, j]:
                current_region = []
                dfs(i, j, current_region)
                regions.append(current_region)
    return regions

def get_bounding_box(region):
    min_row = min(r for r, _ in region)
    max_row = max(r for r, _ in region)
    min_col = min(c for _, c in region)
    max_col = max(c for _, c in region)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find blue regions
    blue_regions = find_regions(input_grid, 1)

    # find bottom blue region
    bottom_blue_region = None
    max_bottom_row = -1

    for region in blue_regions:
      min_row, max_row, min_col, max_col = get_bounding_box(region)
      if max_row > max_bottom_row:
          max_bottom_row = max_row
          bottom_blue_region = region

    # fill bottom with orange, excluding the border
    if bottom_blue_region:
      min_row, max_row, min_col, max_col = get_bounding_box(bottom_blue_region)
      for row in range(min_row+1, max_row):
        for col in range(min_col+1, max_col):
            output_grid[row,col] = 7
            
    # central transformation. 
    # Find and replace within other blue regions
    for region in blue_regions:
        if region != bottom_blue_region:
            min_row, max_row, min_col, max_col = get_bounding_box(region)

            # Check if the region is big enough for the 2x2 red square
            if max_row - min_row >= 3 and max_col - min_col >= 3:
                center_row = (min_row + max_row) // 2
                center_col = (min_col + max_col) // 2

                output_grid[center_row -1 :center_row+1,center_col-1:center_col+1] = 2


    return output_grid
```
