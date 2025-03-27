```python
"""
Transform the input grid by identifying key colored regions and reporting their presence and, partially, their contents.
"""

import numpy as np

def find_objects(grid, background_color):
    """
    Finds contiguous regions of the same color (objects) in the grid.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        return neighbors

    def dfs(r, c, color, object_coords):
        if (r, c) in visited or grid[r, c] != color:
            return
        visited.add((r, c))
        object_coords.append((r, c))
        for nr, nc in get_neighbors(r, c):
            dfs(nr, nc, color, object_coords)

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != background_color and (r, c) not in visited:
                object_coords = []
                dfs(r, c, color, object_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(object_coords)
    return objects

def get_bounding_box(coords):
    """
    Returns the bounding box of a set of coordinates.
    """
    if not coords:
        return (0, 0), (0, 0)
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    return (min_r, min_c), (max_r, max_c)

def transform(input_grid):
    """
    Transforms the input grid based on identified objects and their properties.
    """
    grid = np.array(input_grid)
    background_color = grid[0, 0]  # Assume top-left pixel is background

    objects = find_objects(grid, background_color)

    # Determine output grid size and initialize.  Start with a generous size.
    max_output_rows = 0
    max_output_cols = 0
    
    
    for color in objects:
      for obj_coords in objects[color]:
        (min_r, min_c), (max_r, max_c) = get_bounding_box(obj_coords)
        max_output_rows = max(max_output_rows, max_r - min_r + 1)
        max_output_cols = max(max_output_cols, max_c - min_c + 1)
    

    output_grid = np.full((max_output_rows, max_output_cols * len(objects)), background_color, dtype=int)
    
    
    # Report key objects.
    
    col_offset = 0
    for color in sorted(objects.keys()):
      for obj_coords in objects[color]:       
        (min_r, min_c), (max_r, max_c) = get_bounding_box(obj_coords)
        height = max_r - min_r + 1
        width = max_c - min_c + 1

        # report top of object
        for c in range(width):
          if min_r < output_grid.shape[0] and c + col_offset < output_grid.shape[1]:
            output_grid[min_r, c + col_offset] = grid[min_r,min_c + c]
        
        # report portions of the middle and/or bottom, selectively
        if height > 2:
            for r in range(min_r + 1, max_r):
              for c in range(width):
                if r < output_grid.shape[0] and c + col_offset < output_grid.shape[1]:              
                    output_grid[r, c + col_offset] = grid[r,min_c + c] # default to background

        # report bottom
        if height > 1:
            for c in range(width):
              if max_r < output_grid.shape[0] and c + col_offset < output_grid.shape[1]:
                output_grid[max_r, c + col_offset] = grid[max_r,min_c + c]

      col_offset += width
      
    # remove extra columns/rows
    
    # Find the last row with a non-background pixel
    last_row = -1
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if output_grid[r, c] != background_color:
                last_row = max(last_row, r)

    # Find the last column with a non-background pixel
    last_col = -1
    for c in range(output_grid.shape[1]):
        for r in range(output_grid.shape[0]):
            if output_grid[r, c] != background_color:
                last_col = max(last_col, c)

    if last_row == -1:
      output_grid = np.array([[background_color]]) # return single background
    else:
      output_grid = output_grid[:last_row+1, :last_col+1]

    return output_grid.tolist()
```