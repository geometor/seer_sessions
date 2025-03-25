```python
"""
Identifies contiguous regions of non-zero pixels (shapes) in the input grid,
preserves them in the output grid, and adds a border of '4's above each shape.
The border spans the width of the shape and is repeated multiple times
depending on row position.
"""

import numpy as np

def find_shapes(grid):
    """
    Finds all contiguous shapes in the grid.
    Returns a list of dictionaries, each representing a shape.
    """
    shapes = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, shape_coords):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
            visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        shape_coords.append((r, c))
        dfs(r + 1, c, color, shape_coords)
        dfs(r - 1, c, color, shape_coords)
        dfs(r, c + 1, color, shape_coords)
        dfs(r, c - 1, color, shape_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                shape_coords = []
                dfs(r, c, grid[r, c], shape_coords)
                if shape_coords:
                    min_row = min(coord[0] for coord in shape_coords)
                    max_row = max(coord[0] for coord in shape_coords)
                    min_col = min(coord[1] for coord in shape_coords)
                    max_col = max(coord[1] for coord in shape_coords)
                    shapes.append({
                        "color": grid[r, c],
                        "min_row": min_row,
                        "max_row": max_row,
                        "min_col": min_col,
                        "max_col": max_col,
                        "coords": shape_coords
                    })
    return shapes

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid) # Initialize with zeros

    shapes = find_shapes(input_grid)
    
    # Determine border height based on shape's row position.
    for shape in shapes:
      if shape["min_row"] == 2:
        border_height = 3
      elif shape["min_row"] == 0:
        border_height = 1
      elif shape["min_row"] == 4:
        border_height = 5
      else:
        border_height = 0

      # create new output grid to accommodate border
      new_height = input_grid.shape[0] + border_height
      output_grid = np.zeros((new_height, input_grid.shape[1]), dtype=int)

      # Add borders above each shape.
      for i in range(border_height):
          for col in range(shape["min_col"], shape["max_col"] + 1):
              output_grid[i, col] = 4
    
      # copy the shape to new location
      row_offset = border_height
      for r, c in shape["coords"]:
          output_grid[r + row_offset, c] = input_grid[r,c]
          

    return output_grid
```