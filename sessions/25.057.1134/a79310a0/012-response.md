# a79310a0 • 012 • refine_coder

---
```python
"""
1.  **Identify** all non-zero pixels in the input grid.
2.  **Find** the center of the *output* grid using the output grid dimensions.
3.   For each input pixel that has a non-zero color:
    - a.  Change the color of this pixel to 2 (red).
    - b. Move the pixel to the computed center of the output grid, setting any other pixels in the output grid to 0.
"""

import numpy as np

def find_non_zero_pixels(grid):
    # Iterate through the grid to find all non-zero pixels
    non_zero_pixels = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                non_zero_pixels.append((i, j, grid[i,j]))  # Store coordinates and color
    return non_zero_pixels

def transform(input_grid):
    # Initialize output_grid as a copy of the input, but we will likely overwrite everything
    output_grid = np.zeros_like(input_grid)

    # Find all non-zero pixels and their original colors
    non_zero_pixels = find_non_zero_pixels(input_grid)

    # Find center of output
    center_row = output_grid.shape[0] // 2
    center_col = output_grid.shape[1] // 2

    # If non-zero pixels are found, change color to red and move to center
    if non_zero_pixels:
        output_grid[center_row, center_col] = 2

    return output_grid
```
