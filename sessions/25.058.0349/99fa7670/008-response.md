# 99fa7670 • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify the Center Pixel:** Locate the pixel at the center of the input grid (row 1, column 1, using 0-based indexing).
2.  **Copy Color Value.** Record the color value of the center pixel.
3.  **Replicate to the Right:** Change the color of the pixel directly to the right of the center pixel to match color of the center pixel.
4. **Replicate to Bottom Right**: Change the color of the pixel in the bottom right of the grid to match the color of the center pixel.
5. **Preserve Other Pixels:** All other pixels in the grid retain their original color (white/0).
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
    if center_col + 1 < cols:
      output_grid[center_row, center_col + 1] = center_color
    
    # replicate to bottom right
    if center_row + 1 < rows and center_col + 1 < cols:
      output_grid[center_row + 1, center_col + 1] = center_color
    
    return output_grid
```
