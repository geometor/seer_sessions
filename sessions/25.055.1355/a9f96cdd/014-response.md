# a9f96cdd • 014 • example_3 • investigate_coder

---
```python
"""
1.  **Locate the Red Pixel:** Find the single red (value 2) pixel in the input grid.
2.  **Record Input Position:** Note the row and the column index.
3.  **Create Output Grid:** Initialize an output grid of the same dimensions as the input, filled with zeros (white).
4.  **Place Left Pixel**: Place an azure (8) pixel in the same row, in the column to the immediate *left* of the red pixel. If the red is in the first column, wrap it around to the end.
5.  **Place Right Pixel**: Place an orange (7) pixel in the same row, in the column of to the right of the red pixel. If the red pixel is the right-most column, then place the orange pixel in the first column (0).
6.  **All other pixels:** Remain unchanged (value 0).
"""

import numpy as np

def find_red_pixel(grid):
    # Find the coordinates of the red pixel (value 2).
    rows, cols = np.where(grid == 2)
    if len(rows) > 0:  # Check if a red pixel was found
        return rows[0], cols[0]
    return None  # Return None if no red pixel is found

def transform(input_grid):
    # Create output grid of same dimension, filled with 0
    output_grid = np.zeros_like(input_grid)
    # Find the red pixel.
    red_pixel_coords = find_red_pixel(input_grid)

    if red_pixel_coords:
        row, col = red_pixel_coords
        # Place the azure and orange pixels in output
        rows, cols = input_grid.shape
        output_grid[row, (col - 1) % cols] = 8  # Left, wrap around
        output_grid[row, (col + 1) % cols] = 7  # Right, wrap around

    return output_grid
```
