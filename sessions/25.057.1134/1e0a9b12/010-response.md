# 1e0a9b12 • 010 • refine_coder

---
```python
"""
The transformation rearranges the non-zero pixels in the last column of the input grid to the last column of the output grid, preserving their relative order from bottom to top.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid, but with all last column values set to 0
    output_grid = np.copy(input_grid)
    output_grid[:, -1] = 0

    # Get the last column of the input grid
    last_column = input_grid[:, -1]

    # Extract non-zero pixels from the last column
    non_zero_pixels = last_column[last_column != 0]

    # Get the number of rows in the grid
    num_rows = input_grid.shape[0]

    # Calculate the starting row index for placing non-zero pixels in the output grid, which depends on the grid size, and number of non-zero pixels
    start_row = num_rows - len(non_zero_pixels)

    # Place the non-zero pixels in the last column of the output grid
    if len(non_zero_pixels) > 0:
      output_grid[start_row:, -1] = non_zero_pixels
    

    return output_grid
```
