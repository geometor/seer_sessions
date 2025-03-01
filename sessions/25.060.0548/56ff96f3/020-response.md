# 56ff96f3 • 020 • refine_coder

---
```python
"""
The transformation identifies isolated yellow pixels in the input grid, determines a bounding box 
encompassing these isolated pixels, and then fills this bounding box with yellow pixels in the output grid.
A yellow pixel is considered isolated if all four of its immediate neighbors (up, down, left, and right) are black.
"""

import numpy as np

def is_isolated(grid, row, col):
    """Checks if a yellow pixel at (row, col) is isolated (surrounded by black pixels)."""
    rows, cols = grid.shape
    if grid[row, col] != 4:
        return False

    # Check up
    if row > 0 and grid[row - 1, col] != 0:
        return False
    # Check down
    if row < rows - 1 and grid[row + 1, col] != 0:
        return False
    # Check left
    if col > 0 and grid[row, col - 1] != 0:
        return False
    # Check right
    if col < cols - 1 and grid[row, col + 1] != 0:
        return False

    return True

def get_isolated_yellow_pixels(grid):
    """Finds the coordinates of all isolated yellow pixels in the grid."""
    isolated_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if is_isolated(grid, r, c):
                isolated_pixels.append((r, c))
    return isolated_pixels

def bounding_box(pixels):
    """Calculates the bounding box of a list of pixel coordinates."""
    if not pixels:
        return None
    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')
    for r, c in pixels:
        min_row = min(min_row, r)
        max_row = max(max_row, r)
        min_col = min(min_col, c)
        max_col = max(max_col, c)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """
    Transforms the input grid by identifying isolated yellow pixels, forming a bounding box, and filling it with yellow.
    """
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find isolated yellow pixels
    isolated_yellow_pixels = get_isolated_yellow_pixels(input_grid)

    # Determine bounding box
    if isolated_yellow_pixels:
      top_left, bottom_right = bounding_box(isolated_yellow_pixels)

      # Fill bounding box in output grid
      for r in range(top_left[0], bottom_right[0] + 1):
          for c in range(top_left[1], bottom_right[1] + 1):
              output_grid[r, c] = 4

    return output_grid
```
