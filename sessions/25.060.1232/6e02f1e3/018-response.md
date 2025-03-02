# 6e02f1e3 • 018 • refine_coder

---
```python
"""
The transformation rule is as follows:

1.  Identify the top row of the input grid.
2.  Change the color of all pixels in the top row to gray.
3.  Identify all rows that are not the top row.
4.  Change the color of all pixels the rows that are not the top row to white.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change output pixels 

    # Change the top row to gray (5)
    for j in range(cols):
        output_grid[0, j] = 5

    # Change the remaining rows to white (0)
    for i in range(1, rows):
        for j in range(cols):
            output_grid[i, j] = 0

    return output_grid
```

