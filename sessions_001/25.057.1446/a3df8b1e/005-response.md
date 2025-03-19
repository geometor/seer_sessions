# a3df8b1e • 005 • refine_coder

---
```python
"""
The input grid is transformed to a grid of the same dimensions with a checkerboard pattern. If a checkerboard of blue and black is present, the colors are inverted.
"""

import numpy as np

def is_checkerboard(grid):
    # Check if the grid is a checkerboard pattern of blue (1) and black (0).
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            expected = (i + j) % 2
            if grid[i, j] != expected and grid[i,j] != (1-expected):
                return False, None  # Not a checkerboard, or mixed colors
            if grid[i,j] == 1:
                expected = 1 - expected
            if grid[i,j] != expected:
              return False, None
    return True, 0 # we will always swap 0 and 1

def invert_colors(grid, color1, color2):
    # Invert the specified colors in the grid.
    inverted_grid = np.copy(grid)
    inverted_grid[grid == color1] = -1  # Temporary placeholder
    inverted_grid[grid == color2] = color1
    inverted_grid[inverted_grid == -1] = color2
    return inverted_grid

def transform(input_grid):
    # Initialize output_grid with the same shape as the input.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Check for existing checkerboard and determine inversion colors
    checkerboard, swap_color = is_checkerboard(input_grid)

    if checkerboard:
        output_grid = invert_colors(output_grid, 0, 1)
    else:
        for i in range(rows):
            for j in range(cols):
                output_grid[i,j] = (i+j)%2

    return output_grid
```

