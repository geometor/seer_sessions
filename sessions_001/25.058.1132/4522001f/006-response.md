# 4522001f • 006 • refine_coder

---
```python
"""
1.  Identify the location of the single red pixel (value 2) in the input grid.  The row and column of this pixel determine the dimensions of a square region of green pixels in the output.
2.  The output grid has the same dimensions as the input grid.
3.  Create a square of green (3) pixels in the top-left corner of the output grid. The side length of this square is equal to the row number (0-indexed) of the red pixel in the input grid.
4.  All other pixels in the output grid are set to white (0).
"""

import numpy as np

def find_pixels(grid, color):
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input and filled with white (0)
    output_grid = np.zeros_like(input_grid, dtype=int)

    # Find the red pixel
    red_pixels = find_pixels(input_grid, 2)

    # If a red pixel is found, create the green square
    if len(red_pixels) > 0:
        # Get the row number of the red pixel (this determines the square's side length)
        side_length = red_pixels[0][0]

        # Create the green square
        for r in range(side_length):
            for c in range(side_length):
                output_grid[r, c] = 3

    return output_grid
```
