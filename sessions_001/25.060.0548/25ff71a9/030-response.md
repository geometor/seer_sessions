# 25ff71a9 • 030 • refine_coder

---
```python
"""
1.  **Identify** the red pixel (value 2) in the input grid.
2.  **Find** the row index of the last row of the grid.
3.  **Move** the Red pixel to the last row, keeping the column index the same.
4.  **Return** the modified grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find the coordinates of red pixels
    red_pixels = np.argwhere(input_grid == 2)

    # Move red pixel to last row
    for r, c in red_pixels:
        new_r = height - 1
        new_c = c
        output_grid[r, c] = 0  # Clear old position
        output_grid[new_r, new_c] = 2  # Set new position

    return output_grid
```
