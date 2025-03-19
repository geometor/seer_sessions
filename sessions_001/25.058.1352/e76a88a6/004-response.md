# e76a88a6 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation identifies gray (5) colored objects in the input grid. These gray objects are then replaced with a combination of red (2) and yellow (4) pixels, forming 3x3 squares, and mirrored along the x-axis. The red and yellow pixels form L-shapes within each 3x3 square.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        """Depth-first search to find contiguous pixels of the same color."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append({'color': grid[row, col], 'pixels': obj_pixels})
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Find gray objects
    gray_objects = [obj for obj in objects if obj['color'] == 5]
    
    for gray_object in gray_objects:
      #find the bounding box
      min_row = min(pixel[0] for pixel in gray_object['pixels'])
      max_row = max(pixel[0] for pixel in gray_object['pixels'])
      min_col = min(pixel[1] for pixel in gray_object['pixels'])
      max_col = max(pixel[1] for pixel in gray_object['pixels'])
      
      #ensure its a square, otherwise skip this task instance.
      if (max_row - min_row) != (max_col-min_col):
          continue
      
      # Create the 3x3 replacement square
      replacement_square = np.zeros((3, 3), dtype=int)
      replacement_square[0, 0] = 2
      replacement_square[0, 1] = 2
      replacement_square[0, 2] = 2
      replacement_square[1, 0] = 2
      replacement_square[1, 1] = 4
      replacement_square[1, 2] = 4
      replacement_square[2, 0] = 4
      replacement_square[2, 1] = 4
      replacement_square[2, 2] = 4
      
      #mirror gray objects
      center_row = (min_row + max_row) // 2

      # replace the grey object's pixels
      for r in range(3):
          for c in range(3):
              # Map the replacement square to output coordinates.
              output_row = min_row + r
              output_col = min_col + c

              output_grid[output_row, output_col] = replacement_square[r,c]

    return output_grid
```
