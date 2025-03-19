# 25d8a9c8 • 023 • refine_coder

---
```python
"""
1. Copy the bottom row of the input grid to the bottom row of the output grid.
2. Set all pixels in all other rows of the output grid (i.e., all rows *except* the bottom row) to black (color 0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.  We'll modify it directly.
    output_grid = np.zeros_like(input_grid)

    # Copy the bottom row of the input grid to the bottom row of the output grid.
    output_grid[-1, :] = input_grid[-1, :]

    # Set all rows *except* the bottom row to black (color 0).
    # This is already done by initialization, so we don't have to.
    # output_grid[:-1, :] = 0  # This line is redundant but kept for clarity

    return output_grid
```
