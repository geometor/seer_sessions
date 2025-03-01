# ce9e57f2 • 008 • example_2 • investigate_coder

---
```python
"""
Iterate through the input grid. Identify red (2) pixels. If a red pixel is in rows 6, 7, or 8 and has a red pixel directly above it, change its color to azure (8). Otherwise, keep the original color. Output the modified grid.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for i in range(rows):
        for j in range(cols):
            # Identify red (2) pixels
            if output_grid[i, j] == 2:
                # Check if the current row is one of the bottom three rows (index 5, 6, or 7 which are 6,7,8th rows)
                # and if the pixel above is also red.
                if i >= rows - 3 and i > 0 and output_grid[i - 1, j] == 2:
                    # Change the color to azure (8)
                    output_grid[i, j] = 8

    return output_grid
```
