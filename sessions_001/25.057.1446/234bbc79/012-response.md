# 234bbc79 • 012 • refine_coder

---
```python
"""
Transforms an input grid based on color-specific rules, primarily focusing on
the interaction between vertically adjacent pixels and the influence of gray
pixels as seeds for blue propagation.

1. **Initialization:** The output grid starts as a copy of the input grid.
2. **Identify Seed:** Find all gray (5) pixels in the input grid.
3. **Check Below:** For each gray pixel, check the pixel directly below it.
4. **Initial Replacement:** If the pixel below a gray pixel is *not* black (0), change the gray pixel to blue (1) in the output grid.
5. **Upward Propagation:** Starting from the initially replaced blue pixels, and proceeding upwards row by row:
    *   If a pixel in the output grid is blue (1), and the pixel *directly above* it in the *input* grid is gray(5), change the corresponding pixel in the output grid to blue (1).
6. **Preservation:** Pixels not meeting the above conditions remain unchanged.
"""

import numpy as np

def get_vertically_adjacent_below(grid, row, col):
    """Returns the pixel directly below the given cell, or None if at the bottom."""
    rows, _ = grid.shape
    if row < rows - 1:
        return grid[row + 1, col]
    return None

def get_vertically_adjacent_above(grid, row, col):
    """Returns the pixel directly above the given cell, or None if at the top."""
    if row > 0:
        return grid[row - 1, col]
    return None


def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Identify Seed and Initial Replacement
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:  # Gray pixel
                below = get_vertically_adjacent_below(input_grid, r, c)
                if below != 0 and below is not None:
                    output_grid[r, c] = 1  # Change to blue

    # Upward Propagation
    for r in range(rows - 2, -1, -1): # Iterate upwards, starting from second-to-last row
        for c in range(cols):
            if output_grid[r+1, c] == 1: # if below is blue
                if input_grid[r,c] == 5: # if the input was a gray
                    output_grid[r, c] = 1  # Change to blue
    return output_grid
```
