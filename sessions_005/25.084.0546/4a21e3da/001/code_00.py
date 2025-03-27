"""
Transforms a grid of colored pixels, primarily manipulating orange (7) and blue (1) regions based on the presence of red (2) pixels. The transformation involves mirroring orange regions horizontally and selectively filling areas, while red pixels remain unchanged.
"""

import numpy as np

def get_orange_regions(grid):
    """Identifies and returns a list of orange (7) regions."""
    orange_regions = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_region):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != 7:
            return
        visited[r, c] = True
        current_region.append((r, c))
        dfs(r + 1, c, current_region)
        dfs(r - 1, c, current_region)
        dfs(r, c + 1, current_region)
        dfs(r, c - 1, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 7 and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                orange_regions.append(current_region)
    return orange_regions

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Key Elements
    orange_regions = get_orange_regions(input_grid)

    # 2. Horizontal Mirroring of Orange and Filling
    for region in orange_regions:
        for r, c in region:
            mirrored_c = cols - 1 - c
            if output_grid[r,mirrored_c] == 1:
                output_grid[r, mirrored_c] = 7
    
    # 3. keep original 7's
    for region in orange_regions:
        for r, c in region:
            output_grid[r,c] = 7

    # 4. Red (2) Pixel Preservation
    #   (Already handled by initializing output_grid as a copy)
    for i in range(rows):
      for j in range(cols):
        if output_grid[i,j] == 7:
          # check neighbors
          up = (i-1,j)
          down = (i+1,j)
          left = (i,j-1)
          right = (i,j+1)

          neighbors = [up,down,left,right]

          connected = False
          for nr,nc in neighbors:
            if nr >= 0 and nr < rows and nc >= 0 and nc < cols:
              if input_grid[nr,nc] == 7:
                connected = True
                break

          if not connected:
            output_grid[i,j] = 1
    return output_grid