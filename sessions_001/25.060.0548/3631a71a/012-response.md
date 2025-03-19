# 3631a71a • 012 • refine_coder

---
```python
"""
The transformation rule consistently replaces all '9' (maroon) pixels with '2' (red). The background '0' (white) remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all '9's with '2's.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of the grid.
    for row in range(rows):
        for col in range(cols):
            # If the pixel value is '9', replace it with '2'.
            if input_grid[row, col] == 9:
                output_grid[row, col] = 2

    return output_grid
```
