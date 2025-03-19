# 99fa7670 • 008 • example_2 • investigate_coder

---
```python
"""
1.  Identify the magenta (6) pixel in the input grid.
2.  Copy that magenta pixel to the same position in the output grid.
3.  Add one magenta pixel in the output grid to the right of the original magenta pixel.
4.  Add another magenta pixel in the output grid directly below the original magenta pixel.
5. Leave all the rest pixels of grid as white.
"""

import numpy as np

def find_magenta_pixel(grid):
    # Find the coordinates of the magenta pixel (value 6).
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 6:
                return (i, j)
    return None  # Should not happen in valid cases

def transform(input_grid):
    # Initialize output_grid as a copy of the input.
    output_grid = np.copy(input_grid)

    # Find the magenta pixel.
    magenta_coords = find_magenta_pixel(input_grid)

    if magenta_coords:
        i, j = magenta_coords

        # Add a magenta pixel to the right.
        if j + 1 < output_grid.shape[1]:
            output_grid[i, j + 1] = 6

        # Add a magenta pixel below.
        if i + 1 < output_grid.shape[0]:
            output_grid[i + 1, j] = 6

    return output_grid
```

