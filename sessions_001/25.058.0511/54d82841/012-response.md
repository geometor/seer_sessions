# 54d82841 • 012 • refine_coder

---
```python
"""
A single white pixel at the bottom row is recolored to yellow.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Get the dimensions of the grid
    rows, cols = output_grid.shape

    # Find the white pixel on the bottom row
    bottom_row = output_grid[rows - 1]
    white_pixel_col_index = np.where(bottom_row == 0)[0]

    # verify we found exactly 1 white pixel on bottom row
    if len(white_pixel_col_index) == 1:
      # Change the color of the target pixel to yellow (4)
      target_col = white_pixel_col_index[0]
      output_grid[rows - 1, target_col] = 4
    else:
      # error condition - did not find white pixel on bottom row
      # should not happen with good observations
      print("Error: did not find exactly one white pixel in bottom row.")

    return output_grid
```

