# 794b24be • 024 • refine_coder

---
```python
"""
1. Identify Objects: Find all contiguous regions (shapes) of blue pixels. Consider all other pixels (the background) to be white.
2. Mirror Check: Determine if reflecting the blue shape horizontally creates a valid, mirrored shape. A valid shape extends to the edge of the grid on both sides. The critical difference is the formation of a complete and valid shape. The original shape must extend all the way across.
3. Top Row Transformation: If the blue shape *can* be reflected horizontally to create a complete mirror, change any blue pixels in the *top row* of the *input* grid to red in the output grid. Otherwise, the output grid is identical to the input grid.
"""

import numpy as np

def find_blue_shape(grid):
    """Finds the contiguous region of blue pixels."""
    rows, cols = grid.shape
    blue_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                blue_pixels.append((r, c))
    return blue_pixels

def can_reflect_horizontally(grid, blue_pixels):
    """
    Checks if reflecting the blue shape horizontally would result in a valid,
    mirrored shape.
    """
    if not blue_pixels:
      return False
    
    rows, cols = grid.shape
    
    # Find the min and max columns occupied by blue pixels
    min_col = min(c for _, c in blue_pixels)
    max_col = max(c for _, c in blue_pixels)

    # Check if blue extends to an edge
    if max_col != cols -1:
       return False

    return True

def transform(input_grid):
    """
    Transforms the input grid based on horizontal reflection of the blue shape.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the blue shape
    blue_pixels = find_blue_shape(input_grid)

    # Check if the shape can be reflected
    if can_reflect_horizontally(input_grid, blue_pixels):
        # Transform blue pixels in the top row to red
        for c in range(cols):
            if output_grid[0, c] == 1:
                output_grid[0, c] = 2

    return output_grid
```

