"""
1.  **Identify Green Regions:** Find all contiguous regions of green (3) pixels in the input grid.  Contiguous pixels are connected horizontally or vertically.

2.  **Determine Boundaries:** For each green region, identify its boundary. The boundary consists of pixels that are adjacent to at least one pixel that is not green. Diagonal adjacency does *not* prevent a green from being on the border.

3. **Change the inside of green regions from green to Yellow:** Iterate over all pixels within each identified green region.
    * If the pixel in the region is green and belongs to the boundary of this green region, it does not change, and remains green.
    * If the pixel in the region is green and *not* on the boundary, change its color to yellow (4).

4.  **Preserve Other Colors:**  All pixels that are not green in the input grid remain unchanged in the output grid.

5.  **Output:** The output is the grid resulting from these transformations.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a given color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def is_valid(x, y):
        """Checks if a coordinate is within the grid bounds."""
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_region):
        """Performs Depth-First Search to find contiguous pixels."""
        if not is_valid(x, y) or visited[x, y] or grid[x, y] != color:
            return

        visited[x, y] = True
        current_region.append((x, y))

        # Explore adjacent pixels (up, down, left, right)
        dfs(x + 1, y, current_region)
        dfs(x - 1, y, current_region)
        dfs(x, y + 1, current_region)
        dfs(x, y - 1, current_region)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == color and not visited[x, y]:
                current_region = []
                dfs(x, y, current_region)
                regions.append(current_region)
    return regions

def is_boundary(grid, x, y, region):
    """Checks if a pixel is on the boundary of its region."""
    if (x,y) not in region:
      return False

    rows, cols = grid.shape
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx, ny] != grid[x,y]:
                return True  # Adjacent to a different color
        else:
          return True # Adjacent to a boundary
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()

    # Find green regions
    green_regions = find_contiguous_regions(input_grid, 3)

    # Iterate through each green region
    for region in green_regions:
        # Determine the boundary of the current region
        # boundary_pixels = { (x,y) for x, y in region if is_boundary(input_grid, x, y, region) }

        # Change inner green pixels to yellow
        for x, y in region:
            if not is_boundary(input_grid, x, y, region):
              output_grid[x,y] = 4

    return output_grid