# 31aa019c • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify the Target Object:** Find the non-zero colored object in the input grid that is closest to the bottom-right corner. Prioritize the lowest row first, and on the same row, choose rightmost item.

2.  **Define Highlighted Region:** Once the target object has been found, create a 3x3 square region, centered on the single pixel of the target object which is not zero, furthest to the bottom and right.

3. **Replace with red:** Every value of the 3x3 square will be replaced by the value `2`

4.  **Clear Background:** Set all pixels *outside* the 3x3 highlighted square to 0 (white).

5. **Preserve the center:** If the target object's center was an existing color, preserve that color.
"""

import numpy as np

def find_target_pixel(grid):
    """Finds the target pixel coordinates (bottom-right priority)."""
    rows, cols = grid.shape
    target_pixel = None
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] != 0:
                target_pixel = (r, c)
                return target_pixel # Return immediately when the first is found
    return target_pixel

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.zeros_like(grid)  # Initialize output grid with zeros

    # 1. Find the target pixel
    target_pixel = find_target_pixel(grid)

    if target_pixel is not None:
      # 2. Define the highlighted region (3x3 square)
      r, c = target_pixel
      min_r = max(0, r - 1)
      max_r = min(grid.shape[0], r + 2)
      min_c = max(0, c - 1)
      max_c = min(grid.shape[1], c + 2)

      # 3. Replace with red and preserve center.
      center_color = grid[r,c]

      for i in range(min_r, max_r):
        for j in range(min_c, max_c):
          output_grid[i,j] = 2
      
      output_grid[r,c] = center_color

    return output_grid.tolist()
```
