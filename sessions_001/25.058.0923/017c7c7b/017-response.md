# 017c7c7b • 017 • refine_coder

---
```python
"""
1.  **Identify the Vertical Line:** Find the vertical line of blue (color 1) pixels in the input grid. A vertical line is defined as a contiguous set of pixels of the same color in the same column.

2.  **Change Color:** Change the color of all pixels in the identified vertical line from blue (1) to red (2).

3. **Calculate extension**:
    *   Find the first blue pixel
    *   Determine the number of rows to add:  input height - index of the first blue pixel
4.  **Extend Grid:** Extend the output grid downwards by the calculated amount.

5.  **Fill Extension:** In the newly added rows, fill the cells that are in the same column(s) as the original blue line with red (color 2) pixels. All other cells remain black (color 0).
"""

import numpy as np

def find_first_blue_index(grid):
    # Find the row index of the first blue pixel (color 1) in the grid.
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 1:
               return r
    return -1 # not found

def find_vertical_line(grid, color):
    # Find columns that have at least one pixel of the specified color
    cols_with_color = np.any(grid == color, axis=0)

    # Ensure that all elements in these columns, that are not the background color, equal to color
    for col_idx in np.where(cols_with_color)[0]:
        column = grid[:, col_idx]
        if not np.all((column == color) | (column == 0)):  # Assuming 0 is background
           return None
    # return the index
    return np.where(cols_with_color)[0]

def transform(input_grid):
    # Initialize output_grid as a copy of input and change the color
    output_grid = input_grid.copy()
    output_grid[output_grid == 1] = 2

    # Find the vertical line of blue pixels
    blue_line_cols = find_vertical_line(input_grid, 1)
    first_blue = find_first_blue_index(input_grid)

    # Add three rows for the red
    if blue_line_cols is not None and first_blue != -1:
       num_rows_to_add = input_grid.shape[0] - first_blue
       rows, cols = output_grid.shape
       new_output_grid = np.zeros((rows + num_rows_to_add, cols), dtype=int)
       new_output_grid[:rows,:] = output_grid
       for col in blue_line_cols:
          new_output_grid[rows:,col] = 2
       output_grid = new_output_grid

    return output_grid
```
