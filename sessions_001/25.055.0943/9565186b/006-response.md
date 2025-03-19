# 9565186b • 006 • refine_coder

---
```python
"""
The transformation rule identifies alternating patterns of blue (1) and azure (8) pixels and converts them to gray (5). 
The key is that they must form a checkerboard or alternating sequence, either horizontally or vertically. 
Red (2) pixels remain unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous regions of the same color as objects.
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

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if not visited[i, j]:
                object_pixels = []
                dfs(i, j, grid[i, j], object_pixels)
                if object_pixels:
                    objects.append(
                        {"color": grid[i, j], "pixels": object_pixels}
                    )
    return objects

def is_alternating(grid, pixels):
    """
    Checks if a set of pixels forms an alternating pattern of blue and azure.
    """
    # Check if all pixels are either blue or azure
    colors = [grid[p[0], p[1]] for p in pixels]
    if not all(c in [1, 8] for c in colors):
        return False

    # Check for horizontal alternation
    if len(set(p[0] for p in pixels)) == 1:  # All in the same row
        sorted_pixels = sorted(pixels, key=lambda p: p[1])
        for i in range(len(sorted_pixels) - 1):
            if grid[sorted_pixels[i][0], sorted_pixels[i][1]] == grid[sorted_pixels[i+1][0], sorted_pixels[i+1][1]]:
                return False
        return True

    # Check for vertical alternation
    if len(set(p[1] for p in pixels)) == 1:  # All in the same column
        sorted_pixels = sorted(pixels, key=lambda p: p[0])
        for i in range(len(sorted_pixels) - 1):
            if grid[sorted_pixels[i][0], sorted_pixels[i][1]] == grid[sorted_pixels[i+1][0], sorted_pixels[i+1][1]]:
                return False
        return True

    # check for checkerboard pattern
    rows, cols = zip(*pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    if (max_row - min_row + 1) * (max_col - min_col + 1) != len(pixels):
      return False

    for r in range(min_row, max_row + 1):
      for c in range(min_col, max_col + 1):
          if (r + c) % 2 == 0:
              if grid[r,c] != grid[min_row, min_col]:
                return False
          else:
            if grid[r,c] == grid[min_row, min_col]:
              return False
            
    return True

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Iterate through each object
    for obj in objects:
        # If the object is red, it remains unchanged
        if obj["color"] == 2:
            continue

        # Check if the object forms an alternating pattern
        if is_alternating(input_grid, obj["pixels"]):
            for row, col in obj["pixels"]:
                output_grid[row, col] = 5

    return output_grid
```
