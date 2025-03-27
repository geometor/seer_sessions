```python
"""
The transformation rule identifies 'cross' shaped objects in the input grid and expands them into solid squares of the same color in the output grid.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append(obj)
    return objects

def is_cross_shaped(grid, object_pixels):
    """
    Checks if an object has a 'cross' shape.
    """
    if len(object_pixels) < 5: # optimization: a cross needs at least 5 pixels
      return False

    rows, cols = zip(*object_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    if (max_row - min_row) > 2 or (max_col - min_col) > 2:
      return False

    if len(object_pixels) == 5:
      # check counts of rows and cols
      row_counts = {}
      col_counts = {}

      for r,c in object_pixels:
        row_counts[r] = row_counts.get(r,0) + 1
        col_counts[c] = col_counts.get(c,0) + 1
      
      if len(row_counts) == 3 and len(col_counts) == 3:
        # check that the max counts are 1, except for center element
        for count in row_counts.values():
            if count > 3: # center must be 3
                return False
        for count in col_counts.values():
            if count > 3:
              return False
        return True # its a cross

    return False


def expand_to_square(object_pixels):
    """
    Expands the object to its bounding square.
    """
    rows, cols = zip(*object_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    square_pixels = []
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            square_pixels.append((r, c))
    return square_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find objects
    objects = find_objects(input_grid)
    
    # Process each object
    for obj in objects:
        color = input_grid[obj[0]]
        if is_cross_shaped(input_grid, obj):
            # Expand to square if cross-shaped
            square = expand_to_square(obj)
            for r, c in square:
                output_grid[r, c] = color
        # else skip - no other objects need to be transformed

    return output_grid
```