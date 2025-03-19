# 868de0fa • 022 • example_4 • investigate_coder

---
```python
"""
1. **Identify Blue Regions:** Find all distinct connected regions of blue (1) pixels in the input grid.  Two blue pixels are considered connected if they are adjacent horizontally or vertically (not diagonally).

2.  **Recolor Regions based on shapes:**
      - Recolor the "L"-shaped region blue (1) pixels to orange (7).
      - Recolor the solid rectangular region blue (1) pixels to red (2).

3. **Preserve Background:**  All white (0) pixels in the input grid remain unchanged in the output grid.
"""

import numpy as np

def find_connected_regions(grid, color):
    """Finds connected regions of a specific color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        """Depth-first search to explore a connected region."""
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

        # Explore adjacent cells
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

def is_l_shaped(region, grid):
    """Checks if a region is L-shaped."""
    # Convert region to a set of tuples for easier lookup
    region_set = set(region)

    # Find the bounding box of the region
    min_row = min(r for r, _ in region)
    max_row = max(r for r, _ in region)
    min_col = min(c for _, c in region)
    max_col = max(c for _, c in region)

    # Calculate the expected size of a filled rectangle
    expected_size = (max_row - min_row + 1) * (max_col - min_col + 1)

    # if total grid elements for region are less than the element count of it's bounding box, then its L shaped.
    if len(region) < expected_size:
      return True

    return False

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find connected regions of blue (color 1)
    blue_regions = find_connected_regions(input_grid, 1)

    # Recolor regions based on shape
    for region in blue_regions:
        if is_l_shaped(region, input_grid):
            # Recolor L-shaped regions to orange (7)
            for row, col in region:
                output_grid[row, col] = 7
        else:
            # Recolor other blue regions (assumed to be rectangular) to red (2)
            for row, col in region:
                output_grid[row, col] = 2
    return output_grid
```
