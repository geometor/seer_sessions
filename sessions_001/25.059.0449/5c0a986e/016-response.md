# 5c0a986e • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Find the 2x2 blue square (color 1) and the 2x2 red square (color 2) in the input grid.
2.  **Process Blue Square:** Split the blue square into its four individual blue pixels. Move each of them independently. Place the first blue pixel in the top left of output, and move diagonally down and to the left, one pixel at a time, placing each of the blue pixels.
3.  **Process Red Square:** keep the red pixels in their original relative position, however, move the whole square formation of red, to start in the most right column. Place a red pixel at each location below the red square, and to its right.
"""

import numpy as np

def find_square(grid, color, size=2):
    """Finds a square of a given color and size."""
    rows, cols = grid.shape
    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            if np.all(grid[r:r+size, c:c+size] == color):
                return r, c
    return None, None

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid, filled with white (0).
    output_grid = np.zeros_like(input_grid)

    # Find the blue square.
    blue_row, blue_col = find_square(input_grid, 1)
    if blue_row is not None:
      # Place blue pixels diagonally.
      output_grid[blue_row, 0] = 1
      output_grid[blue_row + 1, 1] = 1
      output_grid[blue_row + 2, 2] = 1
      output_grid[blue_row + 3, 3] = 1

    # Find the red square.
    red_row, red_col = find_square(input_grid, 2)
    if red_row is not None:
        # Place red pixels.
        output_grid[red_row, -2:] = 2
        output_grid[red_row + 1, -2:] = 2
        output_grid[5,-1] = 2
        output_grid[6,-1] = 2


    return output_grid
```
