"""
1.  **Convert Blue to Red:** Change all blue pixels to red.
2.  **Identify Isolated Red Regions:** Find all connected regions of red pixels. A region is isolated if none of its pixels are adjacent (horizontally, vertically, or diagonally) to a green pixel.
3.  **Conditional Green Expansion:** For *each* green pixel in the grid *after* step 1, if it's adjacent (horizontally or vertically) to a red pixel, extend the green vertically (both up and down). Stop the expansion when encountering a background pixel or another green pixel.
4.  **Insert Green to the Left of Isolated Red:** For each isolated red region, find the top row and the leftmost column of the region. Insert green pixels in all columns to the left of the region's leftmost column, starting from the top row of the region.
5. **Expand Inserted Green**: Expand the green inserted (from step 4).
    * From the top row of the isolated red region to the top of the grid.
    * From the bottom row of the isolated red region to the bottom of the grid.
    Stopping expansion at background (8) or other green (3) pixels.
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
                return False
    return True

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Convert Blue to Red
    output_grid[output_grid == 1] = 2

    # 2. Identify Isolated Red Regions
    red_regions = get_connected_regions(output_grid, 2)
    isolated_red_regions = [region for region in red_regions if is_isolated(region, output_grid)]

    # 3. Conditional Green Expansion
    green_pixels = np.argwhere(output_grid == 3)
    for r, c in green_pixels:
        for nr, nc in get_neighbors(output_grid, r, c):
            if output_grid[nr, nc] == 2:
                # Expand upwards
                ur = r - 1
                while ur >= 0 and output_grid[ur, c] != 8 and output_grid[ur,c] != 3:
                    output_grid[ur, c] = 3
                    ur -= 1
                # Expand downwards
                dr = r + 1
                while dr < rows and output_grid[dr, c] != 8 and output_grid[dr,c] != 3:
                    output_grid[dr, c] = 3
                    dr += 1

    # 4. Insert Green to the Left of Isolated Red Regions
    for region in isolated_red_regions:
        min_row = min(r for r, _ in region)
        max_row = max(r for r, _ in region)
        min_col = min(c for _, c in region)
        for c in range(min_col):
            output_grid[min_row, c] = 3

    # 5. Expand Inserted Green
    for region in isolated_red_regions:
      min_row = min(r for r, _ in region)
      max_row = max(r for r, _ in region)
      min_col = min(c for _, c in region)

      # expand up
      ur = min_row - 1
      while ur >= 0:
        all_green = True
        for c in range(min_col):
          if output_grid[ur,c] == 8 or output_grid[ur,c] == 3:
            all_green = False
            break
          else:
            output_grid[ur,c] = 3
        if not all_green:
          break
        ur -= 1
      # expand down
      dr = max_row + 1
      while dr < rows:
        all_green = True
        for c in range(min_col):
          if output_grid[dr,c] == 8 or output_grid[dr,c] == 3:
            all_green = False
            break
          else:
            output_grid[dr,c] = 3
        if not all_green:
          break
        dr += 1

    return output_grid