# b60334d2 • 014 • refine_coder

---
```python
"""
Transforms a 9x9 grid by creating a checkerboard pattern of gray (5) and blue (1) pixels,
starting from the top-left corner. The pattern is a 2x2 block [[5, 1], [1, 0]] repeated
across the grid. The last row and column follow the first row and column of the pattern, respectively.
Remaining cells are filled with white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.zeros_like(input_grid)

    # Create the 2x2 pattern element
    pattern = np.array([[5, 1], [1, 0]])

    # Determine how many times the pattern can fit completely in each dimension
    rows_fit = output_grid.shape[0] // pattern.shape[0]
    cols_fit = output_grid.shape[1] // pattern.shape[1]

    # Expand the pattern in blocks
    for i in range(rows_fit):
        for j in range(cols_fit):
            output_grid[i*2:(i+1)*2, j*2:(j+1)*2] = pattern

    # Handle the last row and column (which are not fully covered by 2x2 blocks)
    if output_grid.shape[0] % 2 != 0:  # Odd number of rows
        for j in range(cols_fit):
            output_grid[8, j*2] = 5   # Gray
            output_grid[8, j*2+1] = 1 # Blue
        if output_grid.shape[1] % 2 != 0:  #Odd Number of columns
            output_grid[8,8] = 5

    if output_grid.shape[1] % 2 != 0:  # Odd number of columns
      if output_grid.shape[0] > 1:
        output_grid[0:rows_fit*2:2, cols_fit*2] = 5
        output_grid[1:rows_fit*2:2, cols_fit*2] = 1


    return output_grid
```
