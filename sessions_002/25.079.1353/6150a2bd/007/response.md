```python
"""
The input grid is rotated 90 degrees clockwise to produce the output grid.  If the input grid is considered as a two-dimensional array, the pixel at `input_grid[x, y]` will be at `output_grid[y, height - 1 - x]`.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((cols, rows), dtype=int)

    # change output pixels 
    for x in range(rows):
        for y in range(cols):
            output_grid[y, rows - 1 - x] = input_grid[x, y]

    return output_grid.tolist()
```