# e48d4e1a • 024 • example_4 • investigate_coder

---
```python
"""
1. **Identify Objects:** Find a cross shape formed by green (3) pixels. The cross consists of a horizontal line and a vertical line. Also locate single gray pixel (5)
2.  **Delete Object:** Delete the gray (5) pixel.
3.  **Shift vertical line:** Shift the vertical line of the green cross one position to the left.
4.  **Maintain:** Keep the horizontal green line in place.
5.  **Output:** Produce the transformed grid.
"""

import numpy as np

def find_cross(grid):
    # Find the horizontal and vertical lines of the cross
    rows, cols = grid.shape
    horizontal_line = None
    vertical_line = None

    for r in range(rows):
        if np.all(grid[r, :] == grid[r, 0]) and grid[r,0] != 0:
            horizontal_line = r
            break

    for c in range(cols):
        if np.all(grid[:, c] == grid[0, c]) and grid[0,c] != 0:
            vertical_line = c
            break

    return horizontal_line, vertical_line

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Delete grey pixel
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 5:
                output_grid[r,c] = 0

    # Find cross
    horizontal_line, vertical_line = find_cross(input_grid)

   # Shift vertical line
    if vertical_line is not None:
        for r in range(rows):
            if output_grid[r, vertical_line] == 3 and r != horizontal_line:
                output_grid[r, vertical_line] = 0
                if vertical_line > 0:
                    output_grid[r, vertical_line - 1] = 3

    return output_grid
```
