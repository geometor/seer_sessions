"""
1.  **Identify Yellow Regions:** Locate all contiguous regions of yellow (4) pixels within the input grid. A contiguous region is defined as a group of one or more yellow pixels connected horizontally or vertically.

2.  **Create Red Border:** For each identified yellow region, create a one-pixel wide border of red (2) pixels around it. This border is created by changing the color of directly adjacent pixels (up, down, left, and right) that were previously white (0). Pixels that are not white should not change.

3. **Output:** The output grid is the modified input grid with the added red borders.
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
    yellow_regions = find_regions(input_grid, 4)

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
            if 0 <= n_row < output_grid.shape[0] and 0 <= n_col < output_grid.shape[1] and output_grid[n_row, n_col] == 0:
              output_grid[n_row, n_col] = 2 # change the cell to red

    return output_grid