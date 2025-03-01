# d9f24cd1 • 002 • example_2 • investigate_coder

---
```python
"""
The transformation overlays a vertical red (2) line pattern onto the input grid, 
while preserving the original x-coordinates (column positions) of any gray (5) pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the base red pattern
    output_grid = np.zeros_like(input_grid)
    for i in range(output_grid.shape[0]):
      for j in range(output_grid.shape[1]):
        if j % 2 == 1:
          output_grid[i][j] = 2

    # Find gray pixels in the input grid and copy their column positions to output
    for row_index, row in enumerate(input_grid):
        for col_index, pixel in enumerate(row):
            if pixel == 5:
                output_grid[row_index, col_index] = 5

    return output_grid
```
