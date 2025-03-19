# 54d82841 • 008 • refine_coder

---
```python
"""
1.  **Identify Target Columns:** Examine the input grid to find all columns that contain one or more magenta (6) pixels. These are the "target columns."
2.  **Transform Magenta Pixels:** Within each target column, change *all* pixels that are magenta (6) to yellow (4).
3.  **Preserve Other Pixels:** All pixels in the grid that are not magenta pixels within the target columns remain unchanged.
"""

import numpy as np

def get_columns_with_color(grid, color):
    """
    Finds the indices of columns containing at least one pixel of the specified color.
    """
    cols = []
    for col in range(grid.shape[1]):
        if np.any(grid[:, col] == color):
            cols.append(col)
    return cols

def transform_magenta_to_yellow(grid, col):
    """
    Changes all magenta pixels in the specified column to yellow.
    """
    for row in range(grid.shape[0]):
        if grid[row, col] == 6:
            grid[row, col] = 4


def transform(input_grid):
    """
    Transforms the input grid according to the observed rule:
    - Identifies columns with magenta pixels.
    - Changes all magenta pixels in those columns to yellow.
    - Keeps all other pixels the same.
    """
    output_grid = np.copy(input_grid)
    magenta_cols = get_columns_with_color(output_grid, 6)

    # Iterate through the identified columns
    for col in magenta_cols:
        # Change all magenta pixels to yellow in the current column
        transform_magenta_to_yellow(output_grid, col)

    return output_grid
```

