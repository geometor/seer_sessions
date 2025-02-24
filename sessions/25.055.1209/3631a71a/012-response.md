# 3631a71a • 012 • refine_coder

---
```python
"""
1.  **Identify Regions:** Locate all contiguous regions of color '9' (maroon) in the input grid.
2.  **Contextual Replacement:** For each maroon region:
    *   If the maroon region is part of a horizontal or vertical series of 9s, replace the maroon pixels with color '1' (blue).
    *   Otherwise, replace each maroon pixel in the identified region with the most frequent color that borders the *entire* region. If there is no border, replace it with '0' (white/blank).
"""

import numpy as np
from collections import Counter

def get_neighbors(grid, row, col):
    """Gets the valid neighbor coordinates and values for a given cell."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j, grid[i, j]))
    return neighbors

def get_region(grid, start_row, start_col, color):
    """
    Finds a contiguous region of the specified color, starting from a given cell.
    Uses Depth-First Search (DFS).
    """
    rows, cols = grid.shape
    region = []
    stack = [(start_row, start_col)]
    visited = set()

    while stack:
        row, col = stack.pop()
        if (row, col) not in visited and 0 <= row < rows and 0 <= col < cols and grid[row, col] == color:
            visited.add((row, col))
            region.append((row, col))

            # Add neighbors to the stack (DFS)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                stack.append((row + dr, col + dc))
    return region
            
def most_common_border_color(grid, region):
    """
    Finds the most common color along the border of the identified region.
    Excludes the color of the region itself.
    """

    border_colors = []
    region_set = set(region) # convert for fast look ups
    region_color = grid[region[0][0]][region[0][1]] # we know the first element exists

    for row, col in region:
        neighbors = get_neighbors(grid, row, col)
        for n_row, n_col, n_color in neighbors:
            if (n_row, n_col) not in region_set:
                border_colors.append(n_color)

    if not border_colors:
        return 0 # default if no border

    most_common = Counter(border_colors).most_common(1)
    return most_common[0][0]

def is_series(grid, region):
    """
    Checks if the region is part of a horizontal or vertical series of 9s.
    """
    rows, cols = grid.shape
    if not region:
      return False

    # Check if all cells in the region are in same row or same col
    first_row, first_col = region[0]
    same_row = all(r == first_row for r, _ in region)
    same_col = all(c == first_col for _, c in region)

    if not (same_row or same_col):
        return False
    
    # Expand the region in horizontal/vertical to check for a series
    if same_row:
      min_col = min(c for _, c in region)
      max_col = max(c for _, c in region)
      for c in range(min_col -1, -1, -1):
          if grid[first_row, c] == 9:
            continue
          else:
            break
      else: # loop completed without breaking - series extended all way to left side
        return True
      for c in range(max_col + 1, cols):
          if grid[first_row, c] == 9:
            continue
          else:
             break
      else:  # series extends to right side
        return True

    if same_col: # check vertical
        min_row = min(r for r, _ in region)
        max_row = max(r for r, _ in region)

        for r in range(min_row -1, -1, -1):
          if grid[r, first_col] == 9:
            continue
          else:
              break
        else: # loop finished, series goes to the top
          return True
        for r in range(max_row + 1, rows):
          if grid[r, first_col] == 9:
            continue
          else:
              break
        else: # series goes to bottom
          return True
    
    return False

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify all '9' regions
    maroon_regions = []
    visited = set()
    for i in range(rows):
        for j in range(cols):
            if input_grid[i,j] == 9 and (i,j) not in visited:
                region = get_region(input_grid, i, j, 9)
                maroon_regions.append(region)
                visited.update(region) # add all cells in region to visited

    # Iterate over '9' regions and replace them
    for region in maroon_regions:
      # check for series
      if is_series(input_grid, region):
        replacement_color = 1
      else:
        # find the most common bordering color
        replacement_color = most_common_border_color(input_grid, region)
      
      # set all pixels in region to the replacement color
      for row, col in region:
          output_grid[row, col] = replacement_color

    return output_grid
```
