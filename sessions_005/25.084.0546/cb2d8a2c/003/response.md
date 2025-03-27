```python
"""
1.  **Replace Blues with Reds:** Change all pixels with the value '1' (blue) to '2' (red).
2.  **Identify Existing Greens:** Locate pixels with a value '3'.
3.  **Expand Existing Green Regions:** For each green (3) pixel, check for adjacent red (2) pixels. If a green pixel is next to a red pixel, expand the green region *vertically* upwards and downwards. Stop the expansion when an '8' (azure) pixel or the grid edge is encountered.
4.  **Identify start row of Isolated Red Regions**: Locate distinct, non-connected regions of red (2) pixels. Find the row index for the start of each red region.
5.  **Insert Green for Isolated Regions:** For each *isolated* red region (those *not* adjacent to any existing green regions *and* not directly adjacent to an expanding 3 region), insert green (3) pixels to the left of this region.
6.  **Extend Inserted Green Vertically:** Extend the newly inserted green pixels vertically (up and down), stopping at an '8' pixel or the grid edge.
7.  **Preserve background** Ensure that untouched '8' pixels remain unchanged.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Get the neighbors of a cell (including diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def get_connected_regions(grid, value):
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
        for nr, nc in get_neighbors(grid, r, c):
            dfs(nr, nc, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == value and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                regions.append(current_region)
    return regions

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Replace Blues with Reds (1 -> 2)
    output_grid[output_grid == 1] = 2

    # Identify Existing Greens
    existing_greens = np.argwhere(output_grid == 3)

    # Expand Existing Green Regions
    for r, c in existing_greens:
        neighbors = get_neighbors(output_grid, r, c)
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

    # Identify Isolated Red Regions
    red_regions = get_connected_regions(output_grid, 2)
    isolated_red_regions = []
    for region in red_regions:
        has_adjacent_green = False
        for r, c in region:
            neighbors = get_neighbors(output_grid, r, c)
            for nr, nc in neighbors:
                if output_grid[nr, nc] == 3:
                    has_adjacent_green = True
                    break
            if has_adjacent_green:
                break
        if not has_adjacent_green:
            isolated_red_regions.append(region)


    # Find Start Rows and insert green for Isolated Regions, extending vertically
    for region in isolated_red_regions:
      # find start row
      min_row = min(r for r, c in region)
      
      # find any adjacent greens after initial expansion
      adj_to_expanded = False
      for r,c in region:
        neighbors = get_neighbors(output_grid, r, c)
        for nr, nc in neighbors:
          if output_grid[nr,nc] == 3:
            adj_to_expanded = True
            break
        if adj_to_expanded:
          break

      if not adj_to_expanded:      
        # insert green to left of region
        first_red_col = min(c for r, c in region)
        for c in range(first_red_col):
            output_grid[min_row, c] = 3

        # expand inserted green up
        ur = min_row - 1
        while ur >= 0 and output_grid[ur, first_red_col -1] != 8:
            for c in range(first_red_col):
              output_grid[ur, c] = 3
            ur -= 1
        # expand inserted green down
        dr = min_row + 1
        while dr < rows and output_grid[dr, first_red_col - 1] != 8:
          for c in range(first_red_col):
            output_grid[dr, c] = 3
          dr += 1
    return output_grid
```