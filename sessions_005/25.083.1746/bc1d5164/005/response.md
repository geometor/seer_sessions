```python
"""
Identifies the non-zero border color of the input grid and constructs a 3x3 output grid.
The output grid mirrors the border color arrangement of the input grid, mapping the top, bottom,
left, and right edges of the input to the corresponding edges of the output.
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
    """Transforms the input grid to a 3x3 output grid based on border colors."""
    border_color = get_border_color(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)

    if border_color is None:
        return output_grid  # Return all zeros if no single border color

    rows, cols = input_grid.shape

    # Map top row of input to top row of output
    for c in range(cols):
      if input_grid[0, c] == border_color:
        output_grid[0, min(c, 2)] = border_color
    
    # Map bottom row of input to bottom row of output
    for c in range(cols):
      if input_grid[rows-1, c] == border_color:
        output_grid[2, min(c,2)] = border_color

    # Map left column of input to left column of output
    for r in range(rows):
        if input_grid[r, 0] == border_color:
            output_grid[min(r, 2), 0] = border_color

    # Map right column of input to right column of output
    for r in range(rows):
        if input_grid[r, cols - 1] == border_color:
            output_grid[min(r, 2), 2] = border_color

    return output_grid
```