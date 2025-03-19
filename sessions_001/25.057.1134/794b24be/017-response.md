# 794b24be • 017 • refine_coder

---
```python
"""
1.  **Initialization:** Start with an output grid that is identical to the input grid.
2.  **Find Blue:** Scan the input grid to find the location of the blue (1) pixel. If no blue pixel is found, the output is all black (0).
3.  **Place Red:** If a blue pixel is found at coordinates (row, col):
    - change the value at (row, col) to black (0)
    - compute the output column index: `output_col = (input_col + x) % input_width` where `x` is calculated by code and `%` is modulus operator.
    - change the pixel in the output grid at (row, `output_col`) to red (2).
4. If no blue pixel is found, return all black.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first occurrence of a specified color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return (r, c)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find Blue
    blue_pixel_coords = find_pixel(input_grid, 1)

    # check that blue pixel was found
    if blue_pixel_coords is not None:
      blue_row, blue_col = blue_pixel_coords

      # Place Red - find the output by trying all offsets
      for offset in range(cols):
         output_col = (blue_col + offset) % cols
         output_grid[blue_row, output_col] = 2

    return output_grid
```
