# 99fa7670 • 012 • refine_coder

---
```python
"""
1.  **Locate**: Find the single magenta (6) pixel in the input grid.
2.  **Create Output**: Create an all-black output grid with the same dimensions as the input.
3. **Draw L**: At the coordinates, add a magenta pixel.
4. **Draw**: add a magenta pixel on the right of the first pixel.
5. **Draw**: add a magenta pixel at the bottom of the original pixel.
"""

import numpy as np

def find_magenta_pixel(grid):
    # Find the coordinates of the magenta pixel (value 6).
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 6:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid as all zeros with the same shape as the input.
    output_grid = np.zeros_like(input_grid)

    # Find the magenta pixel.
    magenta_coords = find_magenta_pixel(input_grid)

    if magenta_coords:
        i, j = magenta_coords

        # Draw the magenta pixel.
        output_grid[i, j] = 6

        # Add a magenta pixel to the right.
        if j + 1 < output_grid.shape[1]:
            output_grid[i, j + 1] = 6

        # Add a magenta pixel below.
        if i + 1 < output_grid.shape[0]:
            output_grid[i + 1, j] = 6

    return output_grid
```
