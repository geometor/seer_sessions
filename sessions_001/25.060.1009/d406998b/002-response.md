# d406998b • 002 • example_4 • investigate_coder

---
```python
"""
Replaces gray (5) pixels with green (3) pixels in alternating columns of the input grid.
The alternation starts from the third column containing a gray pixel.
"""

import numpy as np

def get_columns_with_color(grid, color):
    """
    Returns a list of column indices that contain at least one pixel of the specified color.
    """
    cols_with_color = []
    for j in range(grid.shape[1]):
        if np.any(grid[:, j] == color):
            cols_with_color.append(j)
    return cols_with_color

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = input_grid.copy()
    gray_cols = get_columns_with_color(input_grid, 5)

    if len(gray_cols) >= 3:
       
        start_col = gray_cols[2]

        # Iterate through columns to the right and replace.
        for j in range(start_col, output_grid.shape[1], 3):
            for i in range(output_grid.shape[0]):
                if output_grid[i, j] == 5:
                    output_grid[i, j] = 3

        # Iterate through columns to the left and replace.
        for j in range(start_col - 3, -1, -3):
            for i in range(output_grid.shape[0]):
                if output_grid[i, j] == 5:
                    output_grid[i, j] = 3

    return output_grid
```
