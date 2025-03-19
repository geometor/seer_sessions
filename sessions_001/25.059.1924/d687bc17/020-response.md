# d687bc17 • 020 • refine_coder

---
```python
"""
The transformation preserves a one-pixel thick border of the input grid and clears the interior.  The "clearing" means setting pixels to black (0). The shape of the border is determined by the outer boundary of the input grid.

Specifically, the following algorithm is used:

1.  **Copy**: The input grid is copied to create the output grid. This ensures all initial pixels are preserved.
2.  **Clear Inner Region**: Iterate through all pixels, *excluding* the first and last row, and *excluding* the first and last column. Set the value of these "inner" pixels to 0 (black). This clears the interior region, leaving only the border untouched.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Clear the interior region. Iterate through all rows and columns,
    # excluding the first and last row/column, and set their values to 0.
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            output_grid[r, c] = 0

    return output_grid
```

