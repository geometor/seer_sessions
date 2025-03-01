# ea786f4a • 008 • refine_coder

---
```python
"""
The output grid's pixels are determined based on the sum of their row and column indices (parity). If the sum is even, the output pixel is 0. If the sum is odd, the output pixel is 1. The exception is that if a pixel in the input grid has a value other than 0, its value in the output grid should be the same as in the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # change output pixels based on parity and input value
    for i in range(rows):
        for j in range(cols):
            if input_grid[i][j] != 0:
                output_grid[i, j] = input_grid[i][j]
            elif (i + j) % 2 == 0:
                output_grid[i, j] = 0
            else:
                output_grid[i, j] = 1

    return output_grid
```
