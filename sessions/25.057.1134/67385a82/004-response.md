# 67385a82 • 004 • refine_coder

---
```python
"""
Locates all pixels in the input grid that are colored green (color value 3).
Changes the color of each identified green pixel to azure (color value 8).
Returns the changed grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell in the grid
    for i in range(rows):
        for j in range(cols):
            # Check if the cell is green (color value 3)
            if output_grid[i, j] == 3:
                # Change the cell's color to azure (color value 8)
                output_grid[i, j] = 8

    return output_grid
```

