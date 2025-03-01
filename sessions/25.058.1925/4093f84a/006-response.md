# 4093f84a • 006 • refine_coder

---
```python
"""
The transformation rule is as follows:

1.  **Identify Middle Row:** Find the middle, all-gray row in the input grid. The index of this row will be used for determining the output row.

2.  **Handle Size Differences:** If the input grid has a solid gray row, copy just that row into the output grid in the single middle row.

3. **Handle other rows:** If there isn't a solid gray row, then take all rows except for the very top and very bottom row and change all pixels to gray.

4. **Red pixel rule is no longer needed**
"""

import numpy as np

def find_gray_row(grid):
    # Find rows that are all gray (5)
    for i, row in enumerate(grid):
        if np.all(row == 5):
            return i
    return -1

def transform(input_grid):
    # Find the middle gray row
    gray_row_index = find_gray_row(input_grid)

    if gray_row_index != -1:
        # If a gray row is found, create a single-row output with that row
        output_grid = np.zeros((1, input_grid.shape[1]), dtype=int)
        output_grid[0, :] = input_grid[gray_row_index, :]

        # Create an array with 3 times as many rows
        height = input_grid.shape[0]
        row_middle = height//2
        row_output = gray_row_index - row_middle
        output_grid_mod = np.insert(output_grid, 0, np.full(output_grid.shape[1], 5), axis=0)
        for i in range(0,row_output):
          output_grid_mod = np.insert(output_grid_mod, 0, np.full(output_grid.shape[1], 5), axis=0)

        return output_grid_mod
        

    else:
        # If no gray row is found, copy all rows except the first and last, recoloring to gray
        height = input_grid.shape[0]
        output_grid = np.zeros((height - 2, input_grid.shape[1]), dtype=int)
        for i in range(1, height - 1):
            output_grid[i-1, :] = 5  # Set all pixels in the row to gray
        return output_grid
```
