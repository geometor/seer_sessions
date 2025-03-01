# 3ac3eb23 • 006 • refine_coder

---
```python
"""
The transformation rule is as follows:

1.  Copy the first row of the input grid to the first row of the output grid.
2.  If the input grid has a second row, copy the second row of the input grid to the second row of the output grid.
    If any elements from the first row of the input grid are 2 or 8, and the grid has a second row, those elements are also copied to the second row, maintaining the column index. If an element is not copied from the first row, its value is set to zero. If there is no second row, or if the second row does not exist, skip this step
3. Set all cells in the third row, and all other rows of the output grid to 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with zeros
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Copy the first row from input to output
    output_grid[0, :] = input_grid[0, :]

    # Handle the second row based on the rules
    if rows > 1:
        output_grid[1, :] = input_grid[1,:]
        for j in range(cols):
            if input_grid[0, j] == 2 or input_grid[0, j] == 8:
                output_grid[1, j] = input_grid[0, j]


    # Clear all rows from the third row onwards
    for i in range(2, rows):
        output_grid[i, :] = 0

    return output_grid
```

