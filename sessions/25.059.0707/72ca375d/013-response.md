# 72ca375d • 013 • refine_coder

---
```python
"""
The transformation rule identifies the largest contiguous rectangle of yellow (color 4) pixels in the input grid and extracts it to create the output grid.
"""

import numpy as np

def get_rectangle_dimensions(grid, color):
    """Finds the dimensions of the largest rectangle of the given color."""
    rows, cols = grid.shape
    max_height = 0
    max_width = 0
    start_row = -1
    start_col = -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                # Expand rectangle to the right
                width = 0
                while c + width < cols and grid[r, c + width] == color:
                    width += 1

                # Expand rectangle downwards
                height = 0
                while r + height < rows and np.all(grid[r + height, c:c+width] == color):
                    height += 1

                # Check the overall rect.
                if height * width > max_height * max_width:
                  max_height = height
                  max_width = width
                  start_row = r
                  start_col = c
    return start_row, start_col, max_width, max_height

def transform(input_grid):
    # Find the largest yellow rectangle.
    start_row, start_col, width, height = get_rectangle_dimensions(input_grid, 4)

    # Initialize output
    if start_row == -1:
      return np.array([[]]) # Return an empty array if no yellow rectangle is found

    output_grid = np.zeros((height, width), dtype=int)
    
    # Copy the rectangle.
    for r in range(height):
      for c in range(width):
        output_grid[r,c] = input_grid[start_row+r, start_col+c]

    return output_grid
```
