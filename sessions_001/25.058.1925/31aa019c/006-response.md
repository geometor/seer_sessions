# 31aa019c • 006 • refine_coder

---
```python
"""
1.  **Identify the Target Pixel:** Find the *first* non-zero pixel in the input grid, scanning from top-to-bottom and left-to-right within each row. It doesn't matter *what* the non-zero value is, just that it is not zero.

2.  **Create Highlighted Region:** Create a 3x3 square region centered on the target pixel.

3.  **Color Highlighted Region:** Fill the entire 3x3 square with red (value 2), *except* for the center pixel.

4.  **Preserve Center Pixel:** The center pixel of the 3x3 square retains its original color from the input grid.

5.  **Clear Background:** Set all pixels outside the 3x3 square to 0 (white).
"""

import numpy as np

def find_target_pixel(grid):
    """Finds the target pixel coordinates (top-left priority)."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return (r, c)  # Return immediately when the first is found
    return None

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    grid = np.array(input_grid)
    output_grid = np.zeros_like(grid)

    # 1. Find the target pixel (top-left priority)
    target_pixel = find_target_pixel(grid)

    if target_pixel is not None:
        # 2. Create highlighted region (3x3 square)
        r, c = target_pixel
        min_r = max(0, r - 1)
        max_r = min(grid.shape[0], r + 2)
        min_c = max(0, c - 1)
        max_c = min(grid.shape[1], c + 2)

        # 3. & 4. Color highlighted region and preserve center
        center_color = grid[r, c]
        for i in range(min_r, max_r):
            for j in range(min_c, max_c):
                output_grid[i, j] = 2  # Red
        output_grid[r, c] = center_color

    # 5. Clear background (already done by initializing output_grid to zeros)

    return output_grid.tolist()
```
