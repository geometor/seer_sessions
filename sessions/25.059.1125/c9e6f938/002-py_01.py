"""
The transformation rule involves expanding orange (7) regions horizontally. The expansion doubles the number of 7s, except for single 7 where a mirror is also added. The grid's width is adjusted to accommodate the expanded orange regions, and the new space are filled with white(0).
"""

import numpy as np

def get_orange_regions(grid):
    """
    Identifies and returns the coordinates of orange regions (contiguous blocks of '7's).
    """
    orange_regions = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def dfs(r, c, current_region):
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or grid[r, c] != 7):
            return
        visited[r, c] = True
        current_region.append((r, c))
        dfs(r, c + 1, current_region) # Only check adjacent to right

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 7 and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                orange_regions.append(current_region)
    return orange_regions

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    orange_regions = get_orange_regions(input_grid)

    # Calculate the new width
    new_cols = cols
    if(len(orange_regions) > 0):
      num_7s = sum(len(region) for region in orange_regions)
      adjacent_7_found = False
      for region in orange_regions:
          if len(region) > 1:
            adjacent_7_found = True
            break
      if adjacent_7_found:
        new_cols = cols + num_7s -1
      else:
          new_cols = cols*2
    
    output_grid = np.zeros((rows, new_cols), dtype=int)

    for region in orange_regions:
        if len(region) > 1:
          # double the adjacent 7
          for i, (r, c) in enumerate(region):
              output_grid[r, c] = 7
              output_grid[r, c + len(region)] = 7
        else:
          # expand and mirror 7
          for (r,c) in region:
            output_grid[r, c*2] = 7
            output_grid[r, c*2 + 1] = 7

    return output_grid.tolist()