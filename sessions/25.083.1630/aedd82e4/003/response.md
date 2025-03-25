```python
"""
1.  **Identify and Change Bottom-Right Red:** Find the bottom-most, then right-most, red (2) pixel in the input grid. If found, change it to blue (1).

2.  **Change Next Available Red,** Look for any remaining red(2) pixel starting
    from the top left, moving left to right, and change it to blue(1). If no
    red pixels remain, do nothing more.
"""

import numpy as np

def find_bottom_right_red(grid):
    """Finds the bottom-most, right-most red (2) pixel."""
    rows, cols = grid.shape
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] == 2:
                return (r, c)
    return None

def find_next_red(grid):
    """Finds the next red pixel, searching top-to-bottom, left-to-right."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2:
                return (r, c)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find and change bottom-most, right-most red pixel
    bottom_right_red = find_bottom_right_red(output_grid)
    if bottom_right_red:
        output_grid[bottom_right_red] = 1

    # find and change the next red pixel
    next_red = find_next_red(output_grid)
    if next_red:
        output_grid[next_red] = 1

    return output_grid
```
