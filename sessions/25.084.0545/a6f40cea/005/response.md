```python
"""
Transform the input grid by identifying objects of each color and representing them in the output grid.
The output grid seems to capture a simplified representation of the top and bottom rows of selected objects,
arranged based on color, with a specific spatial relationship.
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
    Transforms the input grid based on identified objects and their properties. The output seems
    to represent a summary of the tops and bottoms of some of the input objects.
    """
    grid = np.array(input_grid)
    background_color = grid[0, 0]  # Assume top-left pixel is background

    objects = find_objects(grid, background_color)

    # Initialize the output grid.  Start with a reasonable, but potentially too-large, size.
    # The examples suggest a fixed number of output rows, related to object properties, but not all.
    
    output_rows = 0
    object_widths = []

    for color in objects:
      for obj_coords in objects[color]:
        (min_r, min_c), (max_r, max_c) = get_bounding_box(obj_coords)
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        output_rows = max(output_rows, height)
        object_widths.append(width)
    
    # output grid will have a column per object
    
    output_grid = np.full((output_rows, sum(object_widths)), background_color, dtype=int)

    # Report key objects.
    col_offset = 0
    for color in sorted(objects.keys()):  # Process colors in sorted order for consistency
      for i, obj_coords in enumerate(objects[color]):
        (min_r, min_c), (max_r, max_c) = get_bounding_box(obj_coords)
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        
        # output top row
        for c in range(width):
          if 0 < output_grid.shape[0] and c + col_offset < output_grid.shape[1]:
            output_grid[0, c + col_offset] = grid[min_r, min_c + c]


        # output the bottom, conditionally, based on height
        if height > 1:
            bottom_row_index = min(height -1, output_grid.shape[0]-1) # ensure within output bounds
            for c in range(width):                
                if bottom_row_index < output_grid.shape[0] and c + col_offset < output_grid.shape[1]:
                  output_grid[bottom_row_index, c + col_offset] = grid[max_r, min_c + c]

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