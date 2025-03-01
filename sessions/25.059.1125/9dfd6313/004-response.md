# 9dfd6313 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation involves moving the value 3 (green) to the place occupied by 5 (gray) in the first row.
Copy other values from input to output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the position of the first '5' and '3'
    pos_3 = None
    pos_5 = None

    for i in range(input_grid.shape[0]):
      for j in range(input_grid.shape[1]):
        if input_grid[i,j] == 3:
            pos_3 = (i, j)
        if input_grid[i,j] == 5:
          pos_5 = (i, j)
          break

    # Swap values in first row only, keep values at other rows
    if pos_3 is not None and pos_5 is not None:
        output_grid[pos_5] = 3
        output_grid[pos_3] = input_grid[pos_5[0],pos_5[1]]

    return output_grid
```
