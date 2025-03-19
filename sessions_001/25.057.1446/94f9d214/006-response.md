# 94f9d214 • 006 • refine_coder

---
```python
"""
The transformation rule is as follows:
1. Iterate through all pixels of the input grid.
2. If a pixel is not white (0), change it to red (2) in the output grid.
3. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid, filled with zeros (white).
    output_grid = np.zeros_like(input_grid, dtype=int)

    # Get the dimensions of the input grid
    rows, cols = input_grid.shape

    # Iterate through all pixels of the input grid
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is not white (0)
            if input_grid[i, j] != 0:
                # If not white, set the corresponding pixel in the output grid to red (2)
                output_grid[i, j] = 2
            else:
                output_grid[i,j] = 0 # explicitly set to zero for clarity

    return output_grid
```

