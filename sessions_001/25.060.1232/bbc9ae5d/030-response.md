# bbc9ae5d • 030 • refine_coder

---
```python
"""
1.  **Extend Height:** The input grid's height (number of rows) is increased to 3.
2.  **Copy First Row:** The first row from the input grid is copied.
3.  **Fill color down:** Each value in the first row of the input grid is copied to the output grid, stacked vertically to the new height of the grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with new height and same width, filled with 0s.
    input_rows, input_cols = input_grid.shape
    output_grid = np.zeros((3, input_cols), dtype=int)
    
    # Fill the new grid by replicating the first row of the input grid.
    for j in range(input_cols):
        for i in range(3):
            output_grid[i, j] = input_grid[0, j]

    return output_grid
```
