# 25d8a9c8 • 012 • refine_coder

---
```python
"""
1. Identify the input grid: This is the initial 2D array of pixels.
2. Find the middle row: Determine the index of the row that is in the center of the grid.
3. Set middle row to gray: Change all pixels in the middle row of the grid to the color gray (value 5).
4. Set other pixels to white: All other pixels in the grid, those not in the middle row, should be changed to white (value 0).
5. Output the modified grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input, filled with white (0).
    output_grid = np.zeros_like(input_grid)

    # Find the middle row index.
    middle_row_index = input_grid.shape[0] // 2

    # Set middle row to gray (5).
    output_grid[middle_row_index, :] = 5

    return output_grid
```

