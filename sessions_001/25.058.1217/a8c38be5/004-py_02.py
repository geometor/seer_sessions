"""
Transforms an input grid by identifying contiguous regions of non-background colors, 
and consolidating these regions into a smaller output grid. The background color (0) 
is removed, and other colored regions are placed into the output grid based on some 
deterministic rules. There is an ordering to how the objects are processed.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous regions (objects) of the same color in a grid, excluding the background (0).
    Returns a dictionary where keys are colors and values are lists of (row, col) coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1,1), (-1,-1), (1,-1),(-1,1)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                color = grid[r][c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)

    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)
    output_grid = np.full((9, 9), -1, dtype=int) # initialize with -1 for empty cells

    # create a flat list of objects, keeping single color instance and position
    flat_objects = []
    for color, object_groups in objects.items():
        for obj in object_groups:
          # compute centroid or min/max for positioning
          row_coords, col_coords = zip(*obj) # Separate row and col coordinates

          # use center coordinates as representative position
          center_r = sum(row_coords) // len(row_coords)
          center_c = sum(col_coords) // len(col_coords)

          flat_objects.append((color, center_r, center_c, len(obj)))

    # order the objects
    # current heuristic: color value, size, then position.
    flat_objects_sorted = sorted(flat_objects, key=lambda x: (x[0], -x[3], x[1], x[2]))
    
    # Place the colors in the output_grid
    
    output_row, output_col = 0, 0

    for color,_,_,_ in flat_objects_sorted:
        
      if output_grid[output_row, output_col] == -1:
          output_grid[output_row, output_col] = color
      else:
        output_grid[output_row, output_col] = color

      # move to the 'next' output grid position.  basic wrap around
      output_col += 1
      if output_col >= 9:
          output_col = 0
          output_row += 1
          if output_row >= 9:
              output_row=0

    output_grid[output_grid == -1] = 5 # fill remaining with a neutral color

    return output_grid.tolist()