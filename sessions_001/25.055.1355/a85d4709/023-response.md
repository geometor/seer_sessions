# a85d4709 • 023 • refine_coder

---
```python
"""
Transforms an input grid based on a checkerboard pattern.  Gray (5) and white (0)
pixels are replaced with green (3) and yellow (4) respectively, based on whether
the sum of their row and column indices is even or odd.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with same dimensions.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel.
    for i in range(rows):
        for j in range(cols):
            # Checkerboard check (even/odd sum of indices).
            if (i + j) % 2 == 0:
                # Even: gray (5) -> green (3), white (0) -> yellow (4).
                if input_grid[i, j] == 5:
                    output_grid[i, j] = 3
                elif input_grid[i, j] == 0:
                    output_grid[i, j] = 4
            else:
                # Odd: gray (5) -> yellow (4), white (0) -> green (3).
                if input_grid[i, j] == 5:
                    output_grid[i, j] = 4
                elif input_grid[i, j] == 0:
                    output_grid[i, j] = 3

    return output_grid
```
