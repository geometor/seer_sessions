# 8403a5d5 • 014 • refine_coder

---
```python
"""
1.  **Locate the Target Pixel:** Examine the input grid and identify *a single* pixel that is either green (3), orange (7), or red (2). Note its row and column coordinates.
2.  **Draw Colored Lines:** In the output grid (of the same dimensions as the input), draw a full horizontal and a full vertical line using the same color as the target pixel identified in step 1. These lines intersect at the coordinates of the target pixel and extend to the edges of the grid.
3.  **Replace the target:** Set the value of the cell at the intersection to '5'.
"""

import numpy as np

def find_target_pixel(grid):
    """Finds the coordinates of the first pixel of a given color (green, orange, or red)."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in (2, 3, 7):
                return (r, c, grid[r,c])  # Return row, col, and color
    return None  # Or handle the case where no target pixel is found

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # 1. Locate the Target Pixel.
    target_pixel_pos = find_target_pixel(input_grid)

    if target_pixel_pos is None:
        return output_grid  # Return empty if no target pixel

    target_row, target_col, target_color = target_pixel_pos

    # 2. Draw Colored Lines.
    for r in range(rows):
        output_grid[r, target_col] = target_color  # Vertical line
    for c in range(cols):
        output_grid[target_row, c] = target_color  # Horizontal line

    # 3. Replace target pixel
    output_grid[target_row, target_col] = 5

    return output_grid
```
