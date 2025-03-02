# ea32f347 • 002 • example_4 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1.  **Identify Shapes:** Scan the input grid and identify all contiguous regions (shapes) of gray (5) pixels.
2.  **Maintain Background:** Keep all white (0) pixels unchanged in the output grid.
3.  **Color Transformation:** For each identified gray shape:
    *   If the grey shape is a vertical line, replace all its pixels with blue (1).
    *   If the grey shape is a horizontal line, replace all its pixels with red (2).
    *   If the grey shape appears as an "L" shape (or can be considered as two perpendicular lines intersecting) - replace its pixels with yellow color (4).
4.  **Output:** The output grid should have the same dimensions as the input grid, with the gray shapes replaced by corresponding colored lines, and the background unchanged.
"""

import numpy as np

def get_objects(grid, color=5):
    """
    Finds contiguous regions of the specified color in the grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or (row, col) in visited
            or grid[row, col] != color
        ):
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def is_vertical_line(obj, grid):
    """Checks if an object is a vertical line."""
    rows, cols = zip(*obj)
    return len(set(cols)) == 1 and len(set(rows)) == len(obj)

def is_horizontal_line(obj, grid):
    """Checks if an object is a horizontal line."""
    rows, cols = zip(*obj)
    return len(set(rows)) == 1 and len(set(cols)) == len(obj)

def is_l_shape(obj, grid):
    """Checks if a shape is an L-shape.  This is a simplification for now."""
    if len(obj) < 3:
        return False
    rows, cols = zip(*obj)
    if len(set(rows)) < len(obj) and len(set(cols)) < len(obj) : # not H or V
      return True
    
    return False
  

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find gray objects
    gray_objects = get_objects(input_grid, color=5)

    # change output pixels 
    for obj in gray_objects:
        if is_vertical_line(obj, input_grid):
            for row, col in obj:
                output_grid[row, col] = 1  # Blue
        elif is_horizontal_line(obj, input_grid):
            for row, col in obj:
                output_grid[row, col] = 2  # Red
        elif is_l_shape(obj, input_grid):
            for row, col in obj:
                output_grid[row, col] = 4  # Yellow
        else:
          # catch all
          for row, col in obj:
            output_grid[row, col] = 4  # Yellow


    return output_grid
```
