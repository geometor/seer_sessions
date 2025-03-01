# 49d1d64f • 010 • example_2 • investigate_coder

---
```python
"""
The input grid is expanded by adding one row above, one row below, one column to the left, and one column to the right. The original grid values are placed inside the new expanded grid, with the top-left corner of the original grid mapping to position (1,1) in the expanded grid (using a 0-indexed system). The top and bottom rows and the leftmost and rightmost columns of the expanded grid are filled with '0' (white). The original border of the input is copied to the border of the expanded grid. Specifically, the first row of the input is replicated and becomes the second row of the expanded grid. The last row of the input is replicated and becomes the row above the bottom row of the expanded grid. The first and last columns of the newly created grid are copied and inserted just before or after themselves.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with expanded dimensions, filled with 0s.
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows + 2, input_cols + 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Copy original grid values to the center of the output grid.
    output_grid[1:output_rows-1, 1:output_cols-1] = input_grid

    # replicate the first and last rows and place
    output_grid[1, 1:output_cols-1] = input_grid[0,:]
    output_grid[-2, 1:output_cols-1] = input_grid[-1,:]

    # expand
    output_rows, output_cols = output_rows, output_cols + 2
    expanded_grid = np.zeros((output_rows, output_cols), dtype=int)
    expanded_grid[:,1:-1] = output_grid

    # replicate the first and last cols and place
    expanded_grid[:, 1] = expanded_grid[:, 2]
    expanded_grid[:, -2] = expanded_grid[:, -3]


    return expanded_grid
```
