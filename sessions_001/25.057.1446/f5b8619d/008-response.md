# f5b8619d • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Expand:** Double the dimensions of the input grid (from 6x6 to 12x12).

2.  **Replicate, with offset:** For every '5' (grey pixel) in the input:
    * Place a corresponding '5' in the same relative, upscaled, position in the output grid. Specifically, an input '5' at (row, col) corresponds to a '5' output at (row\*2, col\*2).

3.  **Frame Create:** Fill a two pixel border all of the value '8' around the perimeter of the output grid.

4.  **Fill Adjacency of replicated 5s:**
    * Place a single 8 on the row above and row below an existing 5, in the same column.
    * Place a single 8 on the column left and right of an existing 5, in the same row.

5. **Fill Remainder:**
    * all empty cells are to have value of 8
"""

import numpy as np

def transform(input_grid):
    # Expand the grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 2, input_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Replicate 5s with offset
    for i in range(input_rows):
        for j in range(input_cols):
            if input_grid[i, j] == 5:
                output_grid[i * 2, j * 2] = 5

    # Frame Create (two-pixel border of 8s)
    output_grid[0:2, :] = 8  # Top two rows
    output_grid[-2:, :] = 8  # Bottom two rows
    output_grid[:, 0:2] = 8  # Left two columns
    output_grid[:, -2:] = 8  # Right two columns

     # Fill Adjacency of replicated 5s
    for i in range(output_rows):
      for j in range(output_cols):
        if output_grid[i,j] == 5:
          if i > 1:
              output_grid[i-1,j] = 8
          if i < output_rows - 2:
              output_grid[i+1, j] = 8
          if j > 1:
              output_grid[i,j-1] = 8
          if j < output_cols - 2:
              output_grid[i, j+1] = 8

    # fill remainder with 8
    for i in range(output_rows):
        for j in range(output_cols):
            if output_grid[i,j] == 0:
                output_grid[i,j] = 8
    return output_grid
```
