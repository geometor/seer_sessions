# 99fa7670 • 010 • refine_coder

---
```python
"""
1.  **Identify the Center Pixel:** Determine the center pixel of the input grid. This is located at `(rows // 2, cols // 2)`, where `rows` and `cols` are the number of rows and columns in the grid, respectively.
2.  **Copy the Center Pixel's Color:** Note the color value of the center pixel.
3. **Replicate to the Right:** Change the value of the grid at the location immediately to the right of the center, at coordinates `(rows // 2, cols // 2 + 1)`, making it equal to the color of the center pixel.
4. **Replicate to the Bottom-Right:** Change the value of the grid at the bottom-right corner, `(rows - 1, cols - 1)` to be equal to the color of the center pixel.
5.  **Preserve Other Pixels:** All other pixels in the grid retain their original color (white/0).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # find center pixel - assumes odd sized grids
    center_row = rows // 2
    center_col = cols // 2
    center_color = input_grid[center_row, center_col]

    # replicate to the right
    output_grid[center_row, center_col + 1] = center_color

    # replicate to bottom right
    output_grid[rows - 1, cols - 1] = center_color

    return output_grid
```

