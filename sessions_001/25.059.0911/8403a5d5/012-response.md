# 8403a5d5 • 012 • refine_coder

---
```python
"""
1.  **Locate the Green Pixel:** Find the single green (3) pixel in the input grid and note its row and column coordinates.
2.  **Draw Green Lines:** In the output grid (which is the same size as the input grid), draw a full horizontal and a full vertical line of green (3) pixels, intersecting at the coordinates found in step 1.  These lines extend to the edges of the grid.
3.  **Replace original pixel:** Replace the pixel where lines intersect (original green pixel) with '5'.
"""

import numpy as np

def find_pixel_by_color(grid, color):
    """Finds the coordinates of the first pixel of a given color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # 1. Locate the Green Pixel.
    green_pixel_pos = find_pixel_by_color(input_grid, 3)

    if green_pixel_pos is None:
        return output_grid  # Return empty if no green pixel

    green_row, green_col = green_pixel_pos

    # 2. Draw Green Lines.
    for r in range(rows):
        output_grid[r, green_col] = 3  # Vertical line
    for c in range(cols):
        output_grid[green_row, c] = 3  # Horizontal line

    # 3. Replace original pixel
    output_grid[green_row, green_col] = 5

    return output_grid
```
