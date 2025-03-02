# 28e73c20 • 034 • refine_coder

---
```python
"""
1.  **Create a Border:** Fill the outermost rows and columns of the input grid with the color green (value 3).
2.  **Create a Cross:**  Within the inner grid (the area remaining after excluding the border), find the central row and central column. Fill these central row(s) and column(s) with the color green (value 3). If there are even numbers of rows, there will be two 'central rows'. Similarly for columns.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros (white), then copy the input grid to the output
    output_grid = np.zeros_like(input_grid)
    output_grid[:] = input_grid

    rows, cols = output_grid.shape

    # Create the border (fill outermost rows and columns with green)
    output_grid[0, :] = 3
    output_grid[rows - 1, :] = 3
    output_grid[:, 0] = 3
    output_grid[:, cols - 1] = 3

    # Create the cross
    # Find the central row(s) and column(s)
    if rows % 2 == 0:  # Even number of rows
        center_rows = [rows // 2 - 1, rows // 2]
    else:  # Odd number of rows
        center_rows = [rows // 2]

    if cols % 2 == 0:  # Even number of columns
        center_cols = [cols // 2 - 1, cols // 2]
    else:  # Odd number of columns
        center_cols = [cols // 2]

    # Fill the central row(s) and column(s) with green, excluding the border
    for r in center_rows:
        for c in range(1, cols - 1):
            output_grid[r, c] = 3
    for c in center_cols:
        for r in range(1, rows - 1):
            output_grid[r, c] = 3

    return output_grid
```
