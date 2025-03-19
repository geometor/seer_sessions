# d23f8c26 • 006 • refine_coder

---
```python
"""
Transforms an input grid by preserving a center vertical line if it exists, preserving a center pixel if it exists, and setting all other pixels to white (0).
"""

import numpy as np

def find_objects(grid):
    """
    Identifies objects in the grid based on contiguous color regions.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, object_pixels):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        object_pixels.append((r, c))
        dfs(r + 1, c, color, object_pixels)
        dfs(r - 1, c, color, object_pixels)
        dfs(r, c + 1, color, object_pixels)
        dfs(r, c - 1, color, object_pixels)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                object_pixels = []
                dfs(r, c, grid[r, c], object_pixels)
                if object_pixels:
                    objects.append({"color": grid[r, c], "pixels": object_pixels})
    return objects

def is_vertical_line(pixels, rows, cols):
    """
    Checks if a set of pixels forms a vertical line spanning the grid's height.
    """
    if len(pixels) != rows:
        return False
    
    # Check unique column
    col_values = [p[1] for p in pixels]
    if len(set(col_values)) != 1:
      return False

    # Check if the line is centered
    if col_values[0] != cols // 2:
        return False

    row_values = sorted([p[0] for p in pixels])
    return row_values == list(range(rows))

def is_center_pixel(pixels, rows, cols):
    """
    Checks if there is only one pixel and if it is at the center of the grid
    """
    return len(pixels) == 1 and pixels[0] == (rows // 2, cols // 2)

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)  # Initialize with white (0)

    objects = find_objects(input_grid)
    
    # handle all the same color, by returning an all 0's grid
    if len(objects) == 1:
      return output_grid

    for obj in objects:
        if is_vertical_line(obj["pixels"], rows, cols):
            for r, c in obj["pixels"]:
                output_grid[r, c] = obj["color"]
        elif is_center_pixel(obj["pixels"], rows, cols):
            r, c = obj["pixels"][0]
            output_grid[r,c] = obj["color"]
    return output_grid
```
