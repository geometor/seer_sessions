# 1b60fb0c • 014 • refine_coder

---
```python
"""
1.  **Identify Blue Objects:** Find all contiguous regions of blue (color 1) pixels. Each contiguous region is considered an object.
2.  **Find Leftmost Vertical Segment:** For each blue object, identify its leftmost vertical segment.
3.  **Determine Segment Pixels:** A vertical segment is defined here as a set of pixels in the leftmost column of the object.
4.  **Change Color:** Change the color of the identified leftmost vertical segment pixels to red (color 2).
5.  **Preserve Other Pixels:** Ensure all other pixels in the grid retain their original colors.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the specified color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj = []
                stack = [(r, c)]
                while stack:
                    row, col = stack.pop()
                    if 0 <= row < rows and 0 <= col < cols and grid[row, col] == color and not visited[row, col]:
                        visited[row, col] = True
                        obj.append((row, col))
                        stack.extend([(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)])
                objects.append(obj)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # find blue objects
    blue_objects = find_objects(input_grid, 1)

    # operate if there is blue object
    for blue_object in blue_objects:
      # find x coordinates of the blue object
      x_coords = [p[1] for p in blue_object]
      min_x = min(x_coords)

      # Identify the sub-shape: leftmost vertical segment of the blue shape.
      sub_shape = []
      for row, col in blue_object:
          if col == min_x:
            sub_shape.append((row,col))

      #change the color of sub_shape
      for row, col in sub_shape:
        output_grid[row, col] = 2

    return output_grid
```
