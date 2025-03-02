# 6e02f1e3 • 032 • refine_coder

---
```python
"""
The transformation creates a new grid of the same size as the input. The main diagonal (from top-left to bottom-right) of this new grid is filled with gray pixels (value 5).  All other pixels in the new grid are white (value 0). The contents of the input grid are ignored.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through the grid and fill the diagonal with 5
    for i in range(min(rows, cols)):
        output_grid[i, i] = 5

    return output_grid
```

