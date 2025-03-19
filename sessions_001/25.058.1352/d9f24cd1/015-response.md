# d9f24cd1 • 015 • refine_coder

---
```python
"""
1.  Identify the gray pixels. These pixels will remain unchanged in the output.
2.  Identify the red pixels in the bottom row of the input grid.
3.  For each red pixel found in the bottom row, change all pixels in that column to red.
4.  Fill the remaining white pixels with red, extending horizontally and vertically to fill the entire grid. Gray pixels block this fill.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the locations of gray (5) pixels.  These remain unchanged.
    gray_pixels = np.where(input_grid == 5)

    # Find original red pixels in the bottom row
    bottom_row_red_pixels = np.where(input_grid[-1, :] == 2)[0]

    # Expand red upwards
    for col in bottom_row_red_pixels:
        output_grid[:, col] = 2

    # Fill the remaining area with red
    output_grid[output_grid == 0] = 2

    return output_grid
```
