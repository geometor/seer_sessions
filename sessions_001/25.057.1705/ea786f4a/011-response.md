# ea786f4a • 011 • refine_coder

---
```python
"""
1. Identify: Examine the input grid.
2. Replace: Create an output grid of the same dimensions as the input, filled entirely with white pixels.
3. Center: Place a single red pixel in the center (1, 1) of the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # change output pixels
    rows, cols = output_grid.shape
    center_row = rows // 2
    center_col = cols // 2
    output_grid[center_row, center_col] = 2

    return output_grid
```
