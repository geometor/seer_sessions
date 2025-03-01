# 54d9e175 • 008 • refine_coder

---
```python
"""
1.  **First Column Transformation (Conditional):**
    *   If *any* pixel in the first column of the input grid is *not* white (0), then change all pixels in the first column of the output grid to orange (7).
    *   If *all* pixels in the first column of the input grid are white (0), then all pixels will be magenta (6), do not change the first column to orange.
2.  **White Pixel Transformation:** Change all white (0) pixels in the input grid to magenta (6) in the output grid.
3.  **Gray Column Preservation:** If a column in the input grid consists entirely of gray (5) pixels, keep that entire column as gray (5) in the output grid.
"""

import numpy as np

def find_gray_columns(grid):
    # Find columns that contain only gray (5) pixels.
    gray_columns = []
    for j in range(grid.shape[1]):
        column = grid[:, j]
        if np.all(column == 5):
            gray_columns.append(j)
    return gray_columns

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input, filled with magenta (6)
    output_grid = np.full_like(input_grid, 6)

    rows, cols = input_grid.shape

    # Find purely gray columns
    gray_columns = find_gray_columns(input_grid)

    # First Column transformation (Conditional)
    first_col_is_all_white = all(input_grid[i, 0] == 0 for i in range(rows))
    if not first_col_is_all_white:
        for i in range(rows):
            output_grid[i, 0] = 7

    # Preserve Gray Column
    for col in gray_columns:
        for i in range(rows):
            output_grid[i, col] = 5

    return output_grid
```
