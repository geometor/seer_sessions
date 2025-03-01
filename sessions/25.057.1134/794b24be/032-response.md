# 794b24be • 032 • example_6 • investigate_coder

---
```python
"""
Iterate through each pixel in the input grid.
If a pixel's value is 1 (blue), change it to 2 (red).
If a pixel's value is 0 (white) keep the pixel's value to 0.
Output the modified grid, preserving the original dimensions.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Get the dimensions of the grid
    rows, cols = output_grid.shape

    # Iterate through each pixel in the grid
    for i in range(rows):
        for j in range(cols):
            # If the pixel is blue (1), change it to red (2)
            if output_grid[i, j] == 1:
                output_grid[i, j] = 2

    return output_grid
```
