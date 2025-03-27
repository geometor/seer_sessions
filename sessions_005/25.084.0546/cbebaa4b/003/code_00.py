"""
Rearrange colored objects within the grid, combining objects of the same color and placing them in the output grid from top to bottom, left to right.
"""

import numpy as np

def find_objects(grid):
    """Finds all contiguous blocks of non-zero pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append((grid[r, c], obj))  # Store color and object pixels
    return objects

def transform(input_grid):
    # Initialize output_grid as all zeros
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Create a dictionary to store the count of each color
    color_counts = {}
    for color, _ in objects:
        color_counts[color] = color_counts.get(color, 0) + 1

    #consolidate by size
    color_counts_by_size = {}
    for color, obj in objects:
      color_counts_by_size[color] = color_counts_by_size.get(color,0) + len(obj)
    

    # Get the list of colors present
    colors_present = sorted(list(color_counts_by_size.keys()))
    
    row_idx = 0
    col_idx = 0
    # Iterate through output grid cells
    
    while True:
      placed = False
      for color in colors_present:
        if color_counts_by_size[color] > 0:
              output_grid[row_idx,col_idx] = color
              color_counts_by_size[color] -= 1
              placed = True
      
      if not placed:
         break

      col_idx += 1
      if col_idx >= cols:
        col_idx = 0
        row_idx += 1
        if row_idx >= rows:
            break

    return output_grid