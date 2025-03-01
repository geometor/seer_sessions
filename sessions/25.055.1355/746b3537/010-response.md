# 746b3537 • 010 • refine_coder

---
```python
"""
Locate objects in the same row as objects of blue and/or red.
If the input contains any rows with blue and/or red objects, extract that row.
Output contains only the selected row, and the order of objects are preserved.
If no blue and/or red on any row, output is an empty 1x1 grid.
"""

import numpy as np

def find_row_with_color(grid, colors):
    """
    Finds the first row index containing any of the specified colors.
    Returns -1 if no row contains any of the colors.
    """
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] in colors:
                return i
    return -1

def transform(input_grid):
    # Find the row containing blue (1) or red (2) objects.
    row_index = find_row_with_color(input_grid, [1, 2])

    # If no such row is found, return a 1x1 empty grid.
    if row_index == -1:
        return np.zeros((1, 1), dtype=int)

    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Initialize the output grid with dimensions 1 x cols.
    output_grid = np.zeros((1, cols), dtype=int)

    # Copy the selected row from the input grid to the output grid.
    output_grid[0, :] = input_grid[row_index, :]

    return output_grid
```

