# e179c5f4 • 012 • refine_coder

---
```python
"""
1. Locate and Replace: Find the single pixel with the value '1' (blue) in the input grid. Replace this pixel with '8' (orange) in the output grid.
2. Checkerboard Pattern:  All other pixels, which have the value '0' (white) in the input grid, are replaced in the output grid based on a checkerboard pattern of '1' (blue) and '8' (azure) that originates from the location of the pixel that was originally '1'. This means that, starting from the original '1' location, adjacent pixels (horizontally, vertically, and diagonally) will alternate between '8' and '1'.
"""

import numpy as np

def find_single_pixel(grid, color):
    """Finds the coordinates of the single pixel with the specified color."""
    pos = np.where(grid == color)
    return pos[0][0], pos[1][0]

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Locate and Replace the '1' with an '8'
    row_1, col_1 = find_single_pixel(input_grid, 1)
    output_grid[row_1, col_1] = 8

    # Checkerboard pattern replacement
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 0:
                if (abs(r - row_1) + abs(c - col_1)) % 2 == 0:
                    output_grid[r, c] = 8
                else:
                    output_grid[r, c] = 1

    return output_grid
```
