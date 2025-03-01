# 4c5c2cf0 • 011 • refine_coder

---
```python
"""
The transformation rule is:
1. Identify Yellow Regions: Find all contiguous regions of yellow pixels within the input grid.
2. Create Red Border: For each identified yellow region, change the color of all
   adjacent pixels, regardless of their original color, to red. Adjacent means
   cells above, below, left and right.
3. Output: Return modified output_grid.
"""

import numpy as np

def find_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    visited = set()
    regions = []

    def dfs(row, col, current_region):
        """Depth-first search to explore a region."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or (row, col) in visited
            or grid[row, col] != color
        ):
            return

        visited.add((row, col))
        current_region.append((row, col))

        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    
    output_grid = np.copy(input_grid)
    yellow_regions = find_regions(input_grid, 4)  # Find all yellow regions

    for region in yellow_regions:
      for row, col in region:
          # Create red border by checking adjacent cells
          neighbors = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
          ]
          
          for n_row, n_col in neighbors:
            # Check boundaries, and change to red regardless of original color.
            if 0 <= n_row < output_grid.shape[0] and 0 <= n_col < output_grid.shape[1]:
              output_grid[n_row, n_col] = 2  # change the cell to red

    return output_grid
```
