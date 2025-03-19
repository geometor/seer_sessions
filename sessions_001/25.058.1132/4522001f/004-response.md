# 4522001f • 004 • example_1 • investigate_coder

---
```python
"""
1.  Identify the red pixel (value 2) in the input grid.
2.  Replace all red pixels with green pixels (value 3).
3.  Expand the green area. Locate original green pixels. Form a 4x4 square from the top left original green pixel, extending to the right and downwards.
4.  Locate the center of the output. Create another 4x4 green square, starting from row 5, col 5, moving downwards and to the right.
5.  All the rest of pixels become white.
"""

import numpy as np

def find_pixels(grid, color):
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize output grid with white (0)
    output_grid = np.zeros((9, 9), dtype=int)

    # Replace red (2) with green (3)
    input_grid[input_grid == 2] = 3

    # Find original green pixels
    green_pixels = find_pixels(input_grid, 3)

    # Create the first 4x4 green square
    if len(green_pixels) >0:
      top_left = green_pixels[0]
      for r in range(4):
          for c in range(4):
              output_grid[top_left[0] + r, top_left[1] + c] = 3

    # Create the second 4x4 green square at row 4, col 4 (shifted from original center)
    for r in range(4):
      for c in range(4):
        output_grid[4+r, 4+c] = 3

    return output_grid
```
