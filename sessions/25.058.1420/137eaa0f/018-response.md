# 137eaa0f • 018 • refine_coder

---
```python
"""
Extracts all non-zero pixels from the input grid and arranges them in a new
output grid. If there are exactly two non-zero pixels, they are placed
diagonally from the top-left. Otherwise, all non-zero pixels are placed
vertically in the first column, starting from the top. The output grid is
trimmed to the minimum size required to contain the non-zero pixels.
"""

import numpy as np

def get_nonzero_pixels(grid):
    """
    Finds the coordinates and values of all non-zero pixels in a grid.

    Args:
        grid: A 2D numpy array representing the input grid.

    Returns:
        A list of tuples, where each tuple contains (row, column, value)
        of a non-zero pixel.
    """
    nonzero_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                nonzero_pixels.append((r, c, grid[r, c]))
    return nonzero_pixels

def transform(input_grid):
    """
    Transforms the input grid based on the rules described above.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # 1. Identify Non-Zero Pixels.
    nonzero_pixels = get_nonzero_pixels(input_grid)
    num_nonzero = len(nonzero_pixels)

    # 2. Create Output Grid (initially large enough, then trim).
    output_grid = np.zeros((num_nonzero, num_nonzero if num_nonzero > 1 else 1), dtype=int)

    # 3. Arrange Pixels.
    if num_nonzero == 2:
        # Diagonal placement.
        output_grid[0, 0] = nonzero_pixels[0][2]
        output_grid[1, 1] = nonzero_pixels[1][2]
        trimmed_output_grid = output_grid[:2, :2] #trim to fit
    elif num_nonzero == 1:
        output_grid[0,0] = nonzero_pixels[0][2]
        trimmed_output_grid = output_grid
    else:
        # Vertical placement in the first column.
        for i in range(num_nonzero):
            output_grid[i, 0] = nonzero_pixels[i][2]
            
        #find dimensions needed
        max_row = 0
        max_col = 0

        for r in range(output_grid.shape[0]):
          for c in range(output_grid.shape[1]):
            if output_grid[r,c] != 0:
              if r > max_row:
                max_row = r
              if c > max_col:
                max_col = c
        trimmed_output_grid = output_grid[:max_row+1,:max_col+1] #trim

    return trimmed_output_grid
```
