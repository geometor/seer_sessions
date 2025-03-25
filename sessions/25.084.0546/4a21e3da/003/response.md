```python
"""
Transforms a grid of colored pixels, primarily manipulating orange (7) and blue (1) regions based on the presence of red (2) pixels. The transformation involves filling areas around orange and red regions to achieve a form of symmetry, with blue pixels acting as a background.
"""

import numpy as np

def get_objects(grid, color):
    """Identifies and returns a list of contiguous regions of the specified color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_bounding_box(region):
    """Calculates the bounding box of a region."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for r, c in region:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return (min_r, min_c), (max_r, max_c)
    

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    output_grid = np.ones_like(input_grid)  # Initialize with blue (1)
    rows, cols = input_grid.shape

    # 1. Identify Key Elements
    orange_regions = get_objects(input_grid, 7)
    red_regions = get_objects(input_grid, 2)

    # 2.  Fill around orange and red
    all_orange_red = []
    for region in orange_regions:
        for r,c in region:
            all_orange_red.append((r,c))
            output_grid[r,c] = 7
    
    for region in red_regions:
        for r,c in region:
            all_orange_red.append((r,c))
            output_grid[r,c] = 2

    
    # Find bounding box
    if len(all_orange_red) > 0:
      (min_r, min_c), (max_r, max_c) = get_bounding_box(all_orange_red)

      # fill the box
      for r in range(min_r, max_r + 1):
          for c in range(min_c, max_c+1):
              if (r,c) in all_orange_red:
                continue
              
              up = (r-1,c)
              down = (r+1, c)
              left = (r, c-1)
              right = (r,c+1)

              neighbors = [up,down,left,right]
              
              orange_count = 0
              for nr,nc in neighbors:
                if nr >= 0 and nr < rows and nc >= 0 and nc < cols:
                  if (nr,nc) in all_orange_red:
                      orange_count += 1

              if orange_count >= 2:
                output_grid[r,c] = 7


    return output_grid
```