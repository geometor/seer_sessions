# caa06a1f • 014 • refine_coder

---
```python
"""
The transformation removes the rightmost column and the bottom row from the input grid IF the input
grid has an even number of rows and columns and the number of rows/columns is less than 5.
Otherwise, the output is a copy of the input.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on its dimensions.
    """
    rows, cols = input_grid.shape

    # Check if the dimensions are even and less than 5.
    if rows % 2 == 0 and cols % 2 == 0 and rows < 5 and cols < 5:
        # Create a copy of the input grid to avoid modifying the original.
        output_grid = np.copy(input_grid)

        # Remove the last row.
        output_grid = output_grid[:-1, :]

        # Remove the rightmost column.
        output_grid = output_grid[:, :-1]
    else:
        # Otherwise, the output is identical to the input.
        output_grid = np.copy(input_grid)

    return output_grid
```

