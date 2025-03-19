# d037b0a7 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation identifies rows containing non-zero values and, for those row, non-zero values are replicated to the next row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replicating non-zero values to the next row.
    """
    output_grid = np.copy(input_grid)  # Initialize output as a copy of the input
    rows, cols = input_grid.shape

    for r in range(rows - 1):  # Iterate through rows up to the second-to-last
        for c in range(cols):
          if input_grid[r,c] != 0:
            output_grid[r+1,c] = input_grid[r,c]


    return output_grid
```
