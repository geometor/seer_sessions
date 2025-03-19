# 5521c0d9 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves identifying colored blocks (non-white pixels) in the input grid, considering them as single combined shape, and rotating this shape 90 degrees counter-clockwise.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous blocks of non-white pixels.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                objects.append(
                    {"color": grid[row, col], "pixels": object_pixels}
                )
    return objects

def rotate_point(point, center):
    """Rotates a point counter-clockwise by 90 degrees around a center."""
    row, col = point
    center_row, center_col = center
    new_row = center_row - (col - center_col)
    new_col = center_col + (row - center_row)
    return new_row, new_col
    

def transform(input_grid):
    """
    Transforms the input grid according to the rotation rule.
    """
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find colored objects
    objects = find_objects(input_grid)

    # Combine all object pixels for rotation
    all_pixels = []
    for obj in objects:
        all_pixels.extend(obj["pixels"])

    if not all_pixels:  # Handle empty input (no objects)
       return output_grid

    # Calculate the centroid of the combined shape
    rows, cols = zip(*all_pixels)
    center_row = sum(rows) / len(rows)
    center_col = sum(cols) / len(cols)
    center = (center_row, center_col)


    # Rotate and place objects in the output grid
    for obj in objects:
      for row, col in obj["pixels"]:
        rotated_row, rotated_col = rotate_point((row, col), center)
        #check that rotated object is not out of bounds
        if 0 <= int(rotated_row) < output_grid.shape[0] and 0 <= int(rotated_col) < output_grid.shape[1]:
          output_grid[int(rotated_row), int(rotated_col)] = obj["color"]
          

    return output_grid
```
