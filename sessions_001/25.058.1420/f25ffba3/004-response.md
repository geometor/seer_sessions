# f25ffba3 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is a reflection across a central horizontal axis,
where the content of the top rows is placed at the bottom rows, and vice versa.
The bottom row of the input now becomes the top row of the output, the second
from bottom row of the input becomes the second from top row of the output and
so on.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get the number of rows
    num_rows = input_grid.shape[0]

    # Reflect the grid across the horizontal axis
    for i in range(num_rows):
      output_grid[i, :] = input_grid[num_rows - 1 - i, :]

    return output_grid
```
