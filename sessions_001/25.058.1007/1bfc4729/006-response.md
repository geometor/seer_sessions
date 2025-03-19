# 1bfc4729 • 006 • refine_coder

---
```python
"""
1.  Identify all non-zero pixels in the input grid.
2.  For each non-zero pixel:
    *   Create a horizontal line by setting all pixels in the pixel's row to the pixel's color.
    *   Create a vertical line by setting all pixels in the pixel's column to the pixel's color.
3. The output grid is formed from applying all lines.
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
            output_grid[r, i] = value

        # Vertical expansion
        for i in range(rows):
            output_grid[i, c] = value

    return output_grid
```
