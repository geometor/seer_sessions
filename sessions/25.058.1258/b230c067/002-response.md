# b230c067 • 002 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Azure Regions:** Locate all contiguous regions of azure (8) pixels in the input grid.
2.  **Determine Replacement Color, first group:** If a region in the top right corner is azure, replace the connected pixels with red (2)
3. **Determine Replacement Color, second group:** replace all other azure pixels with blue (1).
4. **Preserve Background:** Keep all white (0) pixels unchanged.
"""

import numpy as np

def find_contiguous_regions(grid, color):
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

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all azure regions
    azure_regions = find_contiguous_regions(input_grid, 8)

    # Determine replacement color and apply
    for region in azure_regions:
        # initialize as blue, and check for the upper-right corner
        replace_color = 1

        # get the corner pixel for this grid
        max_row = input_grid.shape[0] -1
        max_col = input_grid.shape[1] -1
        corner_pixel = (max_row,max_col)

        # check if there is any overlap with last three rows and cols
        for r, c in region:
          if r >= max_row - 2 and c >= max_col - 2:
            replace_color = 2
            break

        for row, col in region:
            output_grid[row, col] = replace_color

    return output_grid
```
