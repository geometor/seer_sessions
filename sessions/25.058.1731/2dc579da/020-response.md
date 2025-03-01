# 2dc579da • 020 • refine_coder

---
```python
"""
Locate the azure pixel (color code 8) in the input grid. Crop a 5x5 region centered on this pixel.
Within this cropped region, keep only the central azure pixel and set all other pixels to black (0).
"""

import numpy as np

def find_pixel_location(grid, color):
    # Find the location of a pixel with a specific color.
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                return [r, c]
    return None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)

    # Find the location of the azure pixel (color 8).
    azure_location = find_pixel_location(input_grid, 8)

    # Determine the boundaries of the 5x5 crop centered on the azure pixel.
    row_start = azure_location[0] - 2
    row_end = azure_location[0] + 3
    col_start = azure_location[1] - 2
    col_end = azure_location[1] + 3

    # Create an empty 5x5 output grid.
    output_grid = np.zeros((5, 5), dtype=int)

    # Fill the output grid.
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            # Check if the pixel is within the bounds of the original input grid.
            if 0 <= r < input_grid.shape[0] and 0 <= c < input_grid.shape[1]:
                # Calculate the corresponding indices in the output grid.
                output_row = r - row_start
                output_col = c - col_start
                # Keep only the azure pixel, set others to black
                if input_grid[r,c] != 0 and (r,c) == tuple(azure_location):
                  output_grid[output_row, output_col] = input_grid[r, c]
                else:
                  output_grid[output_row,output_col] = 0

    return output_grid.tolist()
```
