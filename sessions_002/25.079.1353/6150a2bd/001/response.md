```python
"""
The input grid is rotated 90 degrees counter-clockwise. Another way to describe it, imagine the grid is two-dimensional array. cell [x, y] becomes cell [width - 1 - y, x].
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # change output pixels 
    for x in range(rows):
        for y in range(cols):
            output_grid[cols - 1 - y, x] = input_grid[x, y]

    return output_grid.tolist()
```
