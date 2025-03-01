# e9afcf9a • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to create an output grid of the same dimensions as the input grid, 
where the values alternate between the values in the first and second rows of the input grid, 
creating a checkerboard pattern.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # change output pixels 
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                output_grid[r, c] = input_grid[0, 0]
            else:
                output_grid[r, c] = input_grid[1, 0]

    return output_grid
```
