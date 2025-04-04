# 1f85a75f • 004 • refine_coder

---
```python
"""
1.  **Identify the Target Object:** Find a contiguous 3x3 block of pixels that all have the same color (any color) within the input grid. Record the color and the top-left coordinates of this block.
2. **Determine Output Size** If a 3x3 block is not found, return a 1x1 grid of 0. If it is found, and has a border of white above and below, return 5 x 3. If it is found and does not have a border, return 3x3.
3.  **Extract Target Object:** Create an output grid based on determined size.
4. **Case 1: No border** 3x3 found, no white border above and below.
    - Fill output grid with the color of the target object.
5. **Case 2: Border** 3x3 found, white border above and below:
   -   Fill the output grid with white (0).
   -   Replace the inner 3x3 portion of the output (rows 1 to 3 and all columns) with the identified color from step 1.
6. Return the output grid.
"""

import numpy as np

def find_3x3_square(grid):
    """Finds a 3x3 square of uniform color."""
    rows, cols = grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            color = grid[r, c]
            if np.all(grid[r:r+3, c:c+3] == color):
                return r, c, color
    return None, None, None

def transform(input_grid):
    """Transforms the input grid based on a 3x3 square."""
    # Find the top-left corner and color of the 3x3 square.
    row, col, color = find_3x3_square(input_grid)

    # If no 3x3 square is found, return a 1x1 grid of 0.
    if row is None:
        return np.zeros((1, 1), dtype=int)

    # Determine output size based on white border above/below
    has_border = False
    if row > 0 and np.all(input_grid[row-1, col:col+3] == 0) and row + 3 < input_grid.shape[0] and np.all(input_grid[row+3, col:col+3] == 0):
            output_grid = np.zeros((5,3), dtype=int)
            has_border = True
    else:
        output_grid = np.full((3, 3), color, dtype=int)

    if has_border:
      output_grid[1:4, :] = color


    return output_grid
```
