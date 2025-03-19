# 25ff71a9 • 028 • refine_coder

---
```python
"""
The transformation rule reflects red pixels across either the horizontal or vertical axis based on the grid's dimensions.

1.  **Examine** the input grid to determine if height is equal to width.
2.  **Identify** the red pixels (value 2) in the input grid.
3.  **If height and width are equal:**
    *   **Reflect** the position of each red pixel across the horizontal axis (x-axis). The new row index will be `height - 1 - old_row_index`, and the column index will remain the same.
4. **If height and width are not equal:**
    *   **Reflect** the position of each red pixel across the vertical axis (y-axis). The new col index will be `width - 1 - old_col_index`, and the row index will remain the same.
5.  **Clear** original positions of the red pixels by making them black.
6. **Update** the position of the red pixels in a copy of the input.
7.  **Return** the modified grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    input_grid_shape = input_grid.shape
    height, width = input_grid_shape

    # Find the coordinates of red pixels
    red_pixels = np.argwhere(input_grid == 2)

    # Determine reflection axis and apply reflection
    if height == width:
        # Reflect across horizontal axis
        for r, c in red_pixels:
            new_r = height - 1 - r
            new_c = c
            output_grid[r, c] = 0  # Clear old position
            output_grid[new_r, new_c] = 2  # Set new position
    else:
        # Reflect across vertical axis
        for r, c in red_pixels:
            new_r = r
            new_c = width - 1 - c
            output_grid[r, c] = 0  # Clear old position
            output_grid[new_r, new_c] = 2  # Set new position

    return output_grid
```
