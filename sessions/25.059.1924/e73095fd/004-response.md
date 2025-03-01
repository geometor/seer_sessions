# e73095fd • 004 • example_1 • investigate_coder

---
```python
"""
The transformation identifies a contiguous shape of gray (5) pixels. It then changes the color of the "interior" gray pixels to yellow (4), while preserving the gray pixels on the border of the shape. The background (white, 0) remains unchanged.
"""

import numpy as np

def get_objects(grid, color):
    """
    Finds contiguous objects of the specified color in the grid.
    Returns a list of pixel coordinates (row, col) that make up each object.
    """
    visited = set()
    objects = []

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
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

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def is_interior(grid, row, col, object_pixels):
    """
    Checks if a pixel at (row, col) is an interior pixel of its object.
    A pixel is interior if it is surrounded by pixels of the same color.
    """
    color = grid[row,col]
    neighbors = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]
    for r, c in neighbors:
        if (
            r < 0
            or r >= grid.shape[0]
            or c < 0
            or c >= grid.shape[1]
            or (r, c) not in object_pixels

        ):
            return False  # Not interior if any neighbor is out of bounds or a different color
    return True


def transform(input_grid):
    """
    Transforms the input grid by filling the interior of a gray (5) shape with yellow (4).
    """
    output_grid = np.copy(input_grid)
    gray_objects = get_objects(input_grid, 5)

    #  expect only one gray object.
    if len(gray_objects) > 0:
      gray_object = gray_objects[0]

      for row, col in gray_object:
          if is_interior(input_grid, row, col, gray_object):
              output_grid[row, col] = 4  # Change interior gray to yellow

    return output_grid
```
