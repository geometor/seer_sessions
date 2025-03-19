# a85d4709 • 008 • refine_coder

---
```python
"""
The transformation rule is as follows:

1. The input and output grids are always 3x3.
2. For each pixel in the input grid, the output color is determined *solely* by the pixel's row index:
    * If the pixel is in row 0, the output color is 3 (green).
    * If the pixel is in row 1, the output color is 4 (yellow).
    * If the pixel is in row 2, the output color is 2 (red).
3. The input pixel's color has *no* effect on the output color; only the row matters.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input.
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate over rows, setting the output color based on row index.
    for i in range(3):
        if i == 0:
            output_grid[i, :] = 3  # Row 0: Green
        elif i == 1:
            output_grid[i, :] = 4  # Row 1: Yellow
        elif i == 2:
            output_grid[i, :] = 2  # Row 2: Red

    return output_grid.tolist()
```
