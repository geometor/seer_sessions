```python
"""
The output grid is 3x3. The border color of the input grid is identified.
If a border pixel is the first non-zero pixel found on the top edge, the
top-middle pixel of the output is set to that color. If a border pixel is the
first non-zero found pixel on the bottom edge, the bottom-middle pixel of the
output is set to that color.  If the first non-zero pixel on the left edge,
the middle-left pixel is set. If the first non-zero pixel on right edge, the
middle-right pixel is set.
"""

import numpy as np

def get_border_color(grid):
    """Finds the single non-zero color on the border of the grid."""
    rows, cols = grid.shape
    border_colors = set()

    for r in range(rows):
        for c in range(cols):
            if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and grid[r, c] != 0:
                border_colors.add(grid[r, c])

    if len(border_colors) == 1:
        return border_colors.pop()
    else:
        return None  # Should ideally only have one border color.

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)
    border_color = get_border_color(input_grid)

    if border_color is None:
      return output_grid

    rows, cols = input_grid.shape

    # Check top border
    for c in range(cols):
        if input_grid[0, c] == border_color:
            output_grid[0, 1] = border_color
            break

    # Check bottom border
    for c in range(cols):
        if input_grid[rows - 1, c] == border_color:
            output_grid[2, 1] = border_color
            break

    # Check left border
    for r in range(rows):
        if input_grid[r, 0] == border_color:
            output_grid[1, 0] = border_color
            break

    # Check right border
    for r in range(rows):
        if input_grid[r, cols - 1] == border_color:
            output_grid[1, 2] = border_color
            break

    return output_grid
```
