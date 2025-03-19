# a3df8b1e • 011 • refine_coder

---
```python
"""
1.  **Identify** the location (row, column) of the single blue pixel in the input grid.
2.  **Create** a diagonal line of blue pixels starting at the identified location.
3.  **Extend** the diagonal line by repeatedly decrementing the row index and incrementing the column index, creating a new blue pixel at each step.
4.  **Continue** extending the diagonal line until the row index reaches 0 or the column index equals the width of the input grid.
5. **Preserve** the location and color of all non-blue pixels from the input grid to the output grid.
"""

import numpy as np

def find_blue_pixel(grid):
    # Find the location of the blue pixel (value 1).
    blue_pixels = np.where(grid == 1)
    if len(blue_pixels[0]) > 0:
        return blue_pixels[0][0], blue_pixels[1][0]
    return None

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the initial blue pixel.
    blue_pixel_location = find_blue_pixel(input_grid)

    if blue_pixel_location:
        row, col = blue_pixel_location

        # Create the diagonal line.
        while row >= 0 and col < input_grid.shape[1]:
            output_grid[row, col] = 1
            row -= 1
            col += 1

    return output_grid
```

