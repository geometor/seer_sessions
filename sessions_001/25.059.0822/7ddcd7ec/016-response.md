# 7ddcd7ec • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify the Core:** Locate the contiguous orange (7) pixels in the input grid. There appears to be an identifiable 2x2 square of '7's.
2.  **Expand:** If there is an isolated orange region, a copy is translated.
3. **Rotate:** The copied orange region rotates by 90 degrees counter-clockwise relative to the 2x2 orange block.
"""

import numpy as np

def find_2x2_square(grid, color):
    """Finds the top-left corner of a 2x2 square of the given color."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r, c] == color and
                grid[r + 1, c] == color and
                grid[r, c + 1] == color and
                grid[r + 1, c + 1] == color):
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the 2x2 orange square
    square_coords = find_2x2_square(input_grid, 7)

    if square_coords:
      r,c = square_coords
      #append a column above and to the right
      output_grid[r-1,c+2] = 7
      output_grid[r-2,c+2] = 7

      #append a column below and to the left
      output_grid[r+2,c-1] = 7
      output_grid[r+3,c-1] = 7


    return output_grid
```
