# 8eb1be9a • 014 • refine_coder

---
```python
"""
The transformation rule involves identifying specific row patterns in the input grid and replicating them in the output grid. The primary patterns are:

1.  **Solid Red Row:** A row consisting entirely of red pixels (color 2).
2.  **Alternating Red/White Row:** A row with an alternating pattern of red and white pixels (colors 2 and 0).

The output grid is generated by replicating either the solid red row or the alternating red/white row, or a combination. If both are present, they are alternated. If neither are present, the grid is filled with 0s.

"""

import numpy as np

def find_solid_row(grid, color):
    """Finds a row that is entirely of the specified color."""
    for row in grid:
        if np.all(row == color):
            return row
    return None

def find_alternating_row(grid, color1, color2):
    """Finds a row with an alternating pattern of two colors."""
    for row in grid:
        if len(np.unique(row)) == 2 and color1 in row and color2 in row:
            if np.all(row[::2] == row[0]) and np.all(row[1::2] == row[1]):
                return row
    return None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # find key rows
    solid_red_row = find_solid_row(input_grid, 2)
    alternating_row = find_alternating_row(input_grid, 0, 2)

    # replicate with alternation
    if solid_red_row is not None and alternating_row is not None:
        row_type = 0  # 0 for solid red, 1 for alternating
        for i in range(height):
            if row_type == 0:
                output_grid[i, :] = solid_red_row
            else:
                output_grid[i, :] = alternating_row
            row_type = 1 - row_type  # Toggle

    elif solid_red_row is not None:
        for i in range(height):
            output_grid[i,:] = solid_red_row

    elif alternating_row is not None:
         for i in range(height):
            output_grid[i,:] = alternating_row

    return output_grid.tolist()
```
