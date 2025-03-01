# 2c608aff • 008 • refine_coder

---
```python
"""
1.  **Identify Yellow Pixels:** Locate all pixels with the color yellow (4).
2.  **Bidirectional Expansion:** For each yellow pixel, extend its color (4) to the left and right.
3.  **Replacement Rule:** During expansion, replace any azure (8) pixels encountered.
4.  **Boundary Condition:** Stop the expansion in each direction (left and right) when a pixel that is *not* azure (8) is encountered.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    return np.argwhere(grid == color)

def transform(input_grid):
    output_grid = np.copy(input_grid)
    yellow_pixels = find_pixels_by_color(input_grid, 4)

    # Iterate through each yellow pixel
    for y_pixel in yellow_pixels:
        row, col = y_pixel

        # Extend to the left
        for c in range(col - 1, -1, -1):
            if output_grid[row, c] == 8:
                output_grid[row, c] = 4
            else:
                break  # Stop if not azure

        # Extend to the right
        for c in range(col + 1, output_grid.shape[1]):
            if output_grid[row, c] == 8:
                output_grid[row, c] = 4
            else:
                break  # Stop if not azure

    return output_grid
```

