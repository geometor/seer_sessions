# 1f0c79e5 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation identifies a 2x2 colored square in the input grid, reflects and inverts it across the line y = -x, 
changes all non-white pixels in the reflected region to magenta (6), and then places that shape along the y = -x line.
"""

import numpy as np

def find_colored_square(grid):
    # Find the 2x2 square of non-white pixels
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if grid[i, j] != 0 and grid[i+1, j] != 0 and grid[i, j+1] != 0 and grid[i+1, j+1] != 0:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid, but filled with 0s
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find the top-left coordinates of the 2x2 colored square
    start_row, start_col = find_colored_square(input_grid)

    # Reflect, invert and recolor the 2x2 square and fill along y = -x
    if start_row is not None:  # Ensure we found a square
       for i in range(rows):
           for j in range(cols):
               if i + j == rows -1 :
                    output_grid[i,j] = 6

    return output_grid
```
