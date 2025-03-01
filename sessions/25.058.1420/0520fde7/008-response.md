# 0520fde7 • 008 • refine_coder

---
```python
"""
1.  **Check Input:** Examine the input grid for two conditions:
    *   The presence of at least one horizontal line consisting entirely of blue (1) pixels.
    *   The presence of at least one vertical line consisting entirely of gray (5) pixels.
2.  **Transformation Rule:** If *both* conditions are met, create a 3x3 output grid.
3. **Output:** Fill the output grid.
      *   Place a red (2) pixel at the center (1, 1).
    *   Fill all other cells in the output grid with white (0).
4. If *either* condition above is *not* met, create a 3x3 output grid filled with white (0)
"""

import numpy as np

def has_horizontal_blue_line(grid):
    """Checks if the grid has at least one horizontal line of blue pixels."""
    for row in grid:
        if all(pixel == 1 for pixel in row):
            return True
    return False

def has_vertical_gray_line(grid):
    """Checks if the grid has at least one vertical line of gray pixels."""
    for j in range(grid.shape[1]):
        if all(grid[:, j] == 5):
            return True
    return False

def transform(input_grid):
    # Initialize a 3x3 output grid filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Check for existence of blue horizontal and gray vertical lines
    if has_horizontal_blue_line(input_grid) and has_vertical_gray_line(input_grid):
        # Place a red (2) pixel at the center (1, 1)
        output_grid[1, 1] = 2

    return output_grid
```
