# 1bfc4729 • 004 • example_1 • investigate_coder

---
```python
"""
1.  Identify all non-zero pixels in the input grid.
2.  For each non-zero pixel:
    *   Create a horizontal line of the same color, extending across the entire row of the pixel's original position.
    *    Create a vertical line of the same color, extending across the entire column of the pixel's original position.
3.  Combine the expanded lines to form the output grid. If a pixel location is altered by more than one expansion, maintain the original non-zero value.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding each non-zero pixel into a horizontal
    and vertical line of the same color.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find non-zero pixels
    non_zero_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_zero_pixels.append((r, c, input_grid[r, c]))

    # Expand each non-zero pixel
    for r, c, value in non_zero_pixels:
        # Horizontal expansion
        for i in range(cols):
          if output_grid[r,i] == 0:
            output_grid[r, i] = value

        # Vertical expansion
        for i in range(rows):
          if output_grid[i,c] == 0:
            output_grid[i, c] = value

    return output_grid
```
