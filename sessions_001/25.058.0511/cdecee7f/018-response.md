# cdecee7f • 018 • refine_coder

---
```python
"""
Identifies a non-zero pixel in the input grid, and creates a 3x3 output grid of the same color.
"""

import numpy as np

def find_first_nonzero_pixel(input_grid):
    """
    Finds the first non-zero pixel in the input grid.
    Returns the color and position of the pixel.
    """
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                return input_grid[r, c], (r, c)
    return 0, None  # Return 0 and None if no non-zero pixel is found

def transform(input_grid):
    # Find the first non-zero pixel and color
    input_grid = np.array(input_grid)
    color, _ = find_first_nonzero_pixel(input_grid)

    # Create a 3x3 output grid using the color, or a 0x0 grid if color is 0
    if color != 0:
      output_grid = np.full((3, 3), color)
    else:
      output_grid = np.zeros((0,0), dtype=int)

    return output_grid
```
