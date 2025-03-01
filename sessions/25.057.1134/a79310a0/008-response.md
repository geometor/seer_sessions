# a79310a0 • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify** the single non-zero pixel in the input grid.
2.  **Change** the value of this pixel to 2 (red).
3.  **Move** this pixel to the center of the grid at coordinates (1,1).
4. **Preserve** the rest of the pixels (value 0 and white) in their orginal positions.
"""

import numpy as np

def find_non_zero_pixel(grid):
    # Iterate through the grid to find the non-zero pixel
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the non-zero pixel
    non_zero_pixel_coords = find_non_zero_pixel(input_grid)

    # If a non-zero pixel is found, change its value to 2 and move it to the center
    if non_zero_pixel_coords:
        # set original position to zero
        output_grid[non_zero_pixel_coords] = 0
        # move to the center and set to 2
        center_row = output_grid.shape[0] // 2
        center_col = output_grid.shape[1] // 2
        output_grid[center_row, center_col] = 2

    return output_grid
```
