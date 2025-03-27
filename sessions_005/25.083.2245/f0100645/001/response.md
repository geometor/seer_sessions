```python
"""
Iterate though each row. Find the left most color and propagate that color to
the adjacent pixel of different value, and then repeat until end of the row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by propagating the leftmost pixel's color across each row.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for r in range(rows):
        seed_color = output_grid[r, 0]  # Get the leftmost pixel's color
        for c in range(1, cols):
            if output_grid[r, c] != seed_color:
                if output_grid[r,c-1] == seed_color:
                  output_grid[r, c] = seed_color


    return output_grid
```