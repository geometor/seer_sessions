# 6430c8c4 • 004 • refine_coder

---
```python
"""
The output grid has the same dimensions as the input grid. Every orange (7) pixel in the input grid is replaced by a green (3) pixel in the output grid. All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.array(input_grid).copy()

    # Iterate through all pixels of the output grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the pixel is orange (7)
            if output_grid[i, j] == 7:
                # Replace orange with green (3)
                output_grid[i, j] = 3

    return output_grid.tolist()
```
