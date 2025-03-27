```python
"""
Iterate through each cell of the input grid. If the color value is either '3' (green) or '4' (yellow), replace it with '6' (magenta). Otherwise, keep the original value. Construct a new output grid by keeping only the first half of each row (columns / 2). Return the modified grid.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell and replace 3 or 4 with 6
    for i in range(rows):
        for j in range(cols):
            if output_grid[i, j] == 3 or output_grid[i, j] == 4:
                output_grid[i, j] = 6

    # Calculate new dimensions: keep rows, and columns / 2 (integer division)
    new_cols = cols // 2

    #resize the output
    output_grid = output_grid[:, :new_cols]

    return output_grid
```