# 54d82841 • 006 • refine_coder

---
```python
"""
1.  **Identify Target Columns:** Scan the input grid to identify all columns that contain one or more magenta (6) pixels.
2.  **Identify lowest magenta pixel:** Within each identified column, identify the magenta pixel that is at the lowest row index within that column.
3.  **Transform to Yellow:** Change the color of that identified pixel to yellow (4).
4.  **Preserve Other Pixels:** All other pixels in the grid remain unchanged.
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

def find_lowest_pixel_of_color(grid, col, color):
    """
    Finds the row index of the lowest pixel of a specified color in a given column.
    Returns -1 if the color is not found in the column.
    """
    row_indices = np.where(grid[:, col] == color)[0]
    if row_indices.size > 0:
        return row_indices[-1]
    else:
        return -1
    

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule:
    - Identifies columns with magenta pixels.
    - Finds the lowest magenta pixel in each of those columns.
    - Changes that lowest magenta pixel to yellow.
    - Keeps all other pixels the same.
    """
    output_grid = np.copy(input_grid)
    magenta_cols = get_columns_with_color(input_grid, 6)

    # Iterate through the identified columns
    for col in magenta_cols:
        # Find the lowest magenta pixel's row index in the current column
        lowest_magenta_row = find_lowest_pixel_of_color(output_grid, col, 6)

        # If a magenta pixel was found in the column, change it to yellow
        if lowest_magenta_row != -1:
          output_grid[lowest_magenta_row, col] = 4

    return output_grid
```

