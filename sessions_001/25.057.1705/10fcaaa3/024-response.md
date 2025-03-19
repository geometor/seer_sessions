# 10fcaaa3 • 024 • refine_coder

---
```python
"""
1.  **Double Grid Size:** Create a new output grid with twice the height and width of the input grid.

2.  **Checkerboard Pattern:** Fill the output grid with a checkerboard pattern of azure (8) and white (0). A cell is colored azure if the sum of its row and column indices is even; otherwise, it is colored white.

3.  **Replicate Red Pixel:** Locate the red pixel (2) in the input grid.
    *   The row index in the output is calculated as: `output_row = input_row * 2 + 1 * (input_row > 0)`.
    *    The column index in the output is calculated as `output_col = if input_row >0 then input_width -1 + input_col else input_width - 2 + input_col`.

4.  There is no need to explicitly fill the remaining with white, since the
    checkerboard pattern will do that by design.
"""

import numpy as np

def transform(input_grid):
    # Double Grid Size.
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Checkerboard Pattern.
    for row in range(output_height):
        for col in range(output_width):
            if (row + col) % 2 == 0:
                output_grid[row, col] = 8  # Azure
            else:
                output_grid[row, col] = 0  # White

    # Replicate Red Pixel.
    red_pixels = np.argwhere(input_grid == 2)
    if len(red_pixels) > 0:
        input_row, input_col = red_pixels[0]
        output_row = input_row * 2 + 1 * (input_row > 0)
        output_col = (input_width - 1 + input_col) if input_row > 0 else (input_width -2 + input_col)
        output_grid[output_row, output_col] = 2

    return output_grid
```
