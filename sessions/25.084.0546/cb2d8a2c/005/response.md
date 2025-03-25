```python
"""
1.  **Convert Blue to Red:** Replace all blue (1) pixels with red (2) pixels.
2.  **Identify Isolated Red Regions:** Before any expansion, identify connected regions of red (2) pixels. A red region is considered "isolated" if none of its pixels are directly adjacent (horizontally, vertically, *or diagonally*) to a green (3) pixel.
3.  **Expand Existing Green Regions Conditionally:** For each existing green (3) pixel, check for adjacent red (2) pixels (horizontally or vertically).
    *   If a red pixel is found adjacent to the green:
        *   Expand the green region vertically upwards from the green pixel, stopping if a background (8) pixel or the edge of the grid is encountered.
        *   Expand the green region vertically downwards from the green pixel, stopping if a background (8) pixel or the edge of the grid is encountered.
4.  **Insert Green to the Left of Isolated Red Regions:** For each *isolated* red region (determined in step 2):
    * Find the top row of each isolated red region.
    *   Insert green (3) pixels to the left of the entire isolated region, starting at the top row and filling all columns to the left of the leftmost red pixel in the region.
5.  **Expand the Inserted Green Vertically:** Extend the newly inserted green pixels (from step 4) vertically (up and down).
    *  Expand upwards, stopping at a background (8) pixel, existing green (3) pixel, or the grid edge.
    *  Expand downwards, stopping at a background (8) pixel, existing green (3) pixel, or the grid edge.
6.  **Preserve Background:** Ensure all background (8) pixels that were not part of any transformation remain unchanged.
"""

import numpy as np

def get_neighbors(grid, r, c, include_diagonal=False):
    """Get the neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if not include_diagonal and (i != 0 and j != 0):
              continue
            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def get_connected_regions(grid, value, include_diagonal=False):
    """Find connected regions of a specific value."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = []

    def dfs(r, c, current_region):
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or visited[r, c]
            or grid[r, c] != value
        ):
            return
        visited[r, c] = True
        current_region.append((r, c))
        for nr, nc in get_neighbors(grid, r, c, include_diagonal):
            dfs(nr, nc, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == value and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                regions.append(current_region)
    return regions

def is_isolated(region, grid):
    """Checks if a region is isolated (not adjacent to green)."""
    for r, c in region:
        for nr, nc in get_neighbors(grid, r, c, include_diagonal=True):
            if grid[nr, nc] == 3:
                return False  # Found an adjacent green pixel
    return True

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Convert Blue to Red
    output_grid[output_grid == 1] = 2

    # 2. Identify Isolated Red Regions (before expansion)
    red_regions = get_connected_regions(output_grid, 2)
    isolated_red_regions = [region for region in red_regions if is_isolated(region, output_grid)]

    # 3. Expand Existing Green Regions Conditionally
    existing_greens = np.argwhere(output_grid == 3)
    for r, c in existing_greens:
        neighbors = get_neighbors(output_grid, r, c)  # Only orthogonal
        for nr, nc in neighbors:
            if output_grid[nr, nc] == 2:
                # Expand vertically upwards
                ur = r - 1
                while ur >= 0 and output_grid[ur, nc] != 8:
                    output_grid[ur, nc] = 3
                    ur -= 1
                # Expand vertically downwards
                dr = r + 1
                while dr < rows and output_grid[dr, nc] != 8:
                    output_grid[dr, nc] = 3
                    dr += 1

    # 4. Insert Green to the Left of Isolated Red Regions
    for region in isolated_red_regions:
        min_row = min(r for r, c in region)
        min_col = min(c for r, c in region)
        for c in range(min_col):
          output_grid[min_row,c] = 3

    # 5. Expand the Inserted Green Vertically
    for region in isolated_red_regions:
        min_row = min(r for r, c in region)
        min_col = min(c for r, c in region)

        # expand up
        ur = min_row - 1
        while ur >= 0 and output_grid[ur, min_col -1] != 8:
          for c in range(min_col):
            if output_grid[ur,c] != 3:
              output_grid[ur,c] = 3
          ur -= 1
        # expand down
        dr = min_row + 1
        while dr < rows and output_grid[dr, min_col-1] != 8:
          for c in range(min_col):
            if output_grid[dr,c] != 3:
              output_grid[dr,c] = 3
          dr += 1

    # 6. Preserve Background (Implicit in the logic)
    return output_grid
```