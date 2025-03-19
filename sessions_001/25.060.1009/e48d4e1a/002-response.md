# e48d4e1a • 002 • example_4 • investigate_coder

---
```python
"""
The transformation identifies a '+' shape formed by intersecting horizontal and vertical lines of the same color.
The vertical line of the '+' is retained in the output, while the horizontal line becomes the second to last row.
"""

import numpy as np

def find_plus_shape(grid):
    rows, cols = grid.shape
    center_row, center_col = -1, -1
    line_color = 0

    # Find the intersection point (center) of the '+' shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                # Check for horizontal and vertical lines
                horizontal_line = all(grid[r, i] == grid[r, c] or grid[r,i] == 0 for i in range(cols))
                vertical_line = all(grid[i, c] == grid[r, c] or grid[i,c] == 0 for i in range(rows))
                if horizontal_line and vertical_line:
                    center_row, center_col = r, c
                    line_color = grid[r, c]
                    break
        if center_row != -1:
            break

    return center_row, center_col, line_color

def transform(input_grid):
    """
    Transforms the input grid by retaining the vertical line of the '+' shape
    and moving the horizontal line to the second-to-last row.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Find the '+' shape and its properties
    center_row, center_col, line_color = find_plus_shape(input_grid)

    if center_row == -1:  # No '+' shape found
        return output_grid
    
    # Copy the vertical line to the output grid.
    for r in range(rows):
      if input_grid[r,center_col] != 0:
        output_grid[r, center_col] = line_color

    # Add the horizontal line to the output grid, second to last.
    for c in range(cols):
        output_grid[rows - 2, c] = line_color

    return output_grid
```
