# 4522001f • 012 • refine_coder

---
```python
"""
1.  **Identify Green Objects:** Find all contiguous regions (objects) of color 3 (green) in the input grid.
2.  **Replicate and Position:** If green objects are present, replicate each distinct green object twice in the output grid:
    *   The first replica should be placed at the top-left corner of the output grid, aligned with the top-left corner.
    *   The second replica should be placed at the bottom-right corner of the output grid, aligned with the bottom-right corner.
3.  **Handle non-green, non-zero values:** If any other non-zero colors exist in the original input image, replace with green (3).
4.  **Preserve Dimensions (if no green):** If no green objects are found in the input, the output grid is identical to the input grid.
5.  **Fill Empty Cells:** Fill the rest with zeros.
"""

import numpy as np

def get_objects(grid):
    """
    Finds connected components (objects) in a grid.
    Returns a list of objects, where each object is a set of (row, col) coordinates, and the color.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object, color):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.add((row, col))
        dfs(row + 1, col, current_object, color)
        dfs(row - 1, col, current_object, color)
        dfs(row, col + 1, current_object, color)
        dfs(row, col - 1, current_object, color)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r,c] != 0:
                current_object = set()
                color = grid[r,c]
                dfs(r, c, current_object, color)
                objects.append((current_object, color))
    return objects

def transform(input_grid):
    # Find objects in the input grid
    objects = get_objects(input_grid)
    
    # Separate green and other objects
    green_objects = [(obj, color) for obj, color in objects if color == 3]
    other_objects = [(obj, color) for obj, color in objects if color != 3 and color != 0]

    if not green_objects:
      if not other_objects:
        return input_grid.copy()

    # Determine output grid size based on input and replication
    input_rows, input_cols = input_grid.shape
    
    max_green_row = 0
    max_green_col = 0

    for obj, _ in green_objects:
      for row, col in obj:
        max_green_row = max(row, max_green_row)
        max_green_col = max(col, max_green_col)

    out_rows = input_rows
    out_cols = input_cols

    if len(green_objects) > 0:
      out_rows = max(input_rows, max_green_row + 1) * 2
      out_cols = max(input_cols, max_green_col + 1) * 2

    output_grid = np.zeros((out_rows, out_cols), dtype=int)
    
    # replace any non-green colors with green
    for obj, color in other_objects:
      for row, col in obj:
          input_grid[row, col] = 3
    green_objects = get_objects(input_grid) # re-calculate after replacement
    
    # Replicate green objects
    for obj, color in green_objects:
        # Get object dimensions
        obj_rows = max(row for row, _ in obj) - min(row for row, _ in obj) + 1
        obj_cols = max(col for _, col in obj) - min(col for _, col in obj) + 1

        # Top-left placement
        for row, col in obj:
            output_grid[row, col] = 3

        # Bottom-right placement

        row_offset = out_rows - obj_rows
        col_offset = out_cols - obj_cols
        for row, col in obj:
            output_grid[row + row_offset, col + col_offset] = 3

    return output_grid
```
