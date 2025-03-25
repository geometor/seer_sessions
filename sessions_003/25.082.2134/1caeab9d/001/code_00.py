"""
The transformation rule involves identifying contiguous blocks of non-zero (non-white) colored pixels in the input grid and consolidating or moving them horizontally. 
Colored blocks of the same color that are not adjacent are made to be adjacent, effectively consolidating them.
The order and relative layout of distinct colored blocks are maintained.
"""

import numpy as np

def get_objects(grid):
    """
    Finds all contiguous blocks of non-zero pixels in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append((grid[row, col], obj))  # Store color and object pixels
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)

    # Get objects from the input grid
    objects = get_objects(input_grid)

    # Sort objects by their row and then column to preserve the original order
    objects_sorted = sorted(objects, key=lambda x: (min(p[0] for p in x[1]), min(p[1] for p in x[1])))


    # group objects by color
    objects_by_color = {}
    for color, obj in objects_sorted:
      if color not in objects_by_color:
        objects_by_color[color] = []
      objects_by_color[color].append(obj)

    # Create new layout, with consolidated objects
    placed_rows = set()
    next_available_row = 0
    for color, object_groups in objects_by_color.items():
      # determine a center row for these objects
      min_row = min(min(p[0] for p in obj)  for obj in object_groups)
      max_row = max(max(p[0] for p in obj) for obj in object_groups)

      while next_available_row in placed_rows and next_available_row <= max_row + len(placed_rows):
        next_available_row += 1

      center_row = (min_row + max_row) // 2

      # Consolidate and place objects by color
      
      consolidated = []
      
      for obj in object_groups:
        consolidated.extend(obj)
      
      consolidated = sorted(consolidated, key = lambda x : (x[0], x[1]))
      
      # compute width of consolidated group
      min_col = min(p[1] for p in consolidated)
      max_col = max(p[1] for p in consolidated)
      object_width = max_col-min_col + 1
      start_col = min_col

      row = max(min_row, next_available_row) # never overlap previous blocks

      # put consolidated object into grid
      current_col = start_col
      for pixel in consolidated:
          output_grid[row, current_col] = color
          current_col += 1
          if current_col >= output_grid.shape[1]: # wrap columns if the go past the end
            current_col = 0
            row += 1
            
      placed_rows.add(row)


    return output_grid