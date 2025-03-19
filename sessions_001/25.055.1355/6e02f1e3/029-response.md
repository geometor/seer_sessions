# 6e02f1e3 • 029 • refine_coder

---
```python
"""
Replace all non-gray pixels on the grid's perimeter with gray.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate over the boundary pixels.
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is on the boundary.
            if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                # Check if the pixel is not gray.
                if output_grid[i, j] != 5:
                    # Replace the pixel with gray.
                    output_grid[i, j] = 5

    return output_grid
```
