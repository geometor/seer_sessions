# fcc82909 • 018 • refine_coder

---
```python
"""
Iterate through all pixels of the input grid. If a pixel is white (0), change it to green (3). Leave all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through all pixels
    for r in range(rows):
        for c in range(cols):
            # If the pixel is white (0), change it to green (3)
            if output_grid[r, c] == 0:
                output_grid[r, c] = 3

    return output_grid
```
