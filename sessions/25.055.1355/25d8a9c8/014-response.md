# 25d8a9c8 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule can be described as a color substitution. Observe each input pixel.
Replace pixels according to these rules:
1. If the pixel is red (2) or white(0), change it to white (0).
2. If the pixel is yellow (4) or maroon(9), change it to gray (5).

This maintains the original 3x3 grid structure while applying a specific color mapping.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2 or input_grid[r,c] == 0:
                output_grid[r, c] = 0
            elif input_grid[r, c] == 4 or input_grid[r, c] == 9:
                output_grid[r, c] = 5
            else:
                output_grid[r,c] = input_grid[r,c] # in case there are colors not specified in color map

    return output_grid
```
