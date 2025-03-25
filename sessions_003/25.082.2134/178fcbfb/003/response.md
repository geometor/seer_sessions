```python
"""
1.  **Identify Target Column(s):** Find the column index (or indices) of the last non-black color(s) encountered when scanning the input grid from top to bottom. The target column is defined as the column where last color from top to bottom appears.

2.  **Replicate Target Column:** Copy the target column(s) vertically, overwriting existing values so each identified target column has the same color pixels as original input on all rows.

3.  **Identify Other Colors:** Identify all colors present in the input grid that are *not* the color of the target column(s). For each of these "other colors," find the row index where it *first* appears in the input grid.

4.  **Fill Rows:** For each "other color," fill the *entire* row where it first appeared with that color.
"""

import numpy as np

def find_target_columns(grid):
    """Finds the column indices of the last non-black color."""
    grid = np.array(grid)
    height, width = grid.shape
    target_columns = []
    last_color = 0

    #find the last color
    for r in range(height -1, -1, -1):
        for c in range(width):
            if grid[r,c] != 0:
                last_color = grid[r,c]
                break;
        if last_color !=0:
            break;

    #find the target columns
    for c in range(width):
        for r in range(height):
            if grid[r,c] == last_color:
                target_columns.append(c)
                break;

    return target_columns, last_color

def find_other_colors(grid, target_color):
    """Finds colors other than the target color and their first row index."""
    grid = np.array(grid)
    height, width = grid.shape
    other_colors = {}
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0 and color != target_color and color not in other_colors:
                other_colors[color] = r
    return other_colors

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Identify Target Column(s)
    target_columns, target_color = find_target_columns(input_grid)

    # Replicate Target Column
    for c in target_columns:
        for r in range(height):
            output_grid[r,c] = input_grid[r,c]


    # Identify Other Colors
    other_colors = find_other_colors(input_grid, target_color)

    # Fill Rows with Other Colors
    for color, row_index in other_colors.items():
        output_grid[row_index, :] = color

    return output_grid.tolist()
```