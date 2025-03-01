# ff805c23 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation identifies a repeating color pattern within the input grid, 
finds the bounding box of the primary colored object, determines the corner
pattern, extracts relevant pixels, and creates a downsized output grid based
on the object and corner pattern.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of the same color in the grid.
    Returns a dictionary where keys are colors and values are lists of pixel coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                obj = []
                dfs(r, c, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)

    return objects

def bounding_box(obj):
    """
    Calculates the bounding box of a list of pixel coordinates.
    Returns (min_row, min_col, max_row, max_col).
    """
    if not obj:
        return None
    min_row = min(p[0] for p in obj)
    min_col = min(p[1] for p in obj)
    max_row = max(p[0] for p in obj)
    max_col = max(p[1] for p in obj)
    return (min_row, min_col, max_row, max_col)

def get_corner_colors(grid):
    """
    Returns the colors of the four corners of the grid.
    """
    rows, cols = grid.shape
    return [grid[0, 0], grid[0, cols - 1], grid[rows - 1, 0], grid[rows - 1, cols - 1]]
    

def transform(input_grid):
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Determine corner colors
    corner_colors = get_corner_colors(input_grid)
    
    # Determine primary object and its bounding box. Here, use the top-left corner color for demo
    primary_color = corner_colors[0]
    largest_object = []
    for obj_list in objects.get(primary_color, []):  # Use get to handle cases where color might not exist
      if len(obj_list) > len(largest_object):
          largest_object = obj_list
          
    bbox = bounding_box(largest_object)
    
    if not bbox:
      return np.array([[input_grid[0,0]]]) # Handle case if primary color not found
    
    min_r, min_c, max_r, max_c = bbox

    output_grid_height = max_r - min_r + 1
    output_grid_width =  max_c - min_c + 1

    # Attempt to infer output grid dimensions based on input and bounding box
    output_grid_height = 5
    output_grid_width = 5

    #Initialize the output grid
    output_grid = np.zeros((output_grid_height, output_grid_width), dtype=int)
    
    for r in range(output_grid_height):
      for c in range(output_grid_width):
          # Map the output grid indices to the input grid indices
          in_r = min_r + (r * (max_r - min_r) // (output_grid_height -1) if output_grid_height>1 else 0)
          in_c = min_c + (c * (max_c - min_c) // (output_grid_width -1) if output_grid_width > 1 else 0)

          if input_grid[in_r, in_c] in corner_colors:
            output_grid[r,c] = input_grid[in_r, in_c]

    return output_grid
```
