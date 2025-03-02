# ba97ae07 • 024 • refine_coder

---
```python
"""
Examine the input grid and identify green (3) pixels that are directly to the right of red (2) pixels.
Change these green pixels to black (0) in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid, checking for green pixels to the right of red pixels.
    for i in range(rows):
        for j in range(cols - 1):  # Check up to the second-to-last column
            if input_grid[i, j] == 2 and input_grid[i, j + 1] == 3:
                # Change the green pixel to black.
                output_grid[i, j + 1] = 0

    return output_grid
```
