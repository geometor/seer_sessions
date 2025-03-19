# 49d1d64f • 004 • example_1 • investigate_coder

---
```python
"""
Expands each pixel of the input grid into a 2x2 block in the output grid,
maintaining the original color. Adds a one-pixel wide white (0) border around
the entire output grid and between the 2x2 blocks.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as 4x4 with all zeros
    output_grid = np.zeros((4, 4), dtype=int)

    # iterate through input grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # expand each pixel to a 2x2 block in output, separated by zeros
            output_grid[2*i + 1, 2*j + 1] = input_grid[i, j]
            output_grid[2*i, 2*j+1] = input_grid[i,j]
            output_grid[2*i+1, 2*j] = input_grid[i,j]

    return output_grid
```
