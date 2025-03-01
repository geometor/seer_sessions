# 57aa92db • 026 • refine_coder

---
```python
"""
The input grid is transformed as follows:

1. **Green Pixel Expansion:**  The single green pixel, if present, expands into a shape where it moves one pixel to the left, and one pixel diagonally up and to the left.  The original pixel remains.
2. **Yellow 2x2 Square Expansion:** The 2x2 yellow square expands downward, covering the area where a 2x2 red square might be located directly below it. If a red 2x2 square exists directly below the yellow one, it is replaced by yellow. The yellow square expands two rows downward regardless of whether there are red pixels.
3. **Other Objects:**  All other objects, specifically single azure pixels, 2x2 azure squares and any red objects not directly below a yellow 2x2, remain in their original positions.
"""

import numpy as np

def find_single_pixel_object(grid, color):
    """Finds all instances of a single pixel of the given color."""
    rows, cols = grid.shape
    pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                pixels.append((r, c))
    return pixels

def find_2x2_square(grid, color):
    """Finds the top-left corner of all 2x2 squares of a given color."""
    rows, cols = grid.shape
    squares = []
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r, c] == color and grid[r + 1, c] == color and
                grid[r, c + 1] == color and grid[r + 1, c + 1] == color):
                squares.append((r, c))
    return squares

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Green Pixel Expansion
    green_pixels = find_single_pixel_object(input_grid, 3)
    for r, c in green_pixels:
        # new pixels
        if c > 0:
            output_grid[r, c - 1] = 3  # to the left
        if r > 0 and c > 0:
            output_grid[r - 1, c - 1] = 3  # diagonally up and left

    # 2. Yellow 2x2 Square Expansion
    yellow_squares = find_2x2_square(input_grid, 4)
    for r, c in yellow_squares:
        # Expand down by two rows, replacing any 2x2 red squares
        for i in range(2):
            for j in range(2):
              if r + 2 < rows:
                output_grid[r + 2 + i, c + j] = 4
              if r + 3 < rows:
                output_grid[r + 2 + i + 1, c + j] = 4

    return output_grid
```
