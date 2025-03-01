# aedd82e4 • 006 • refine_coder

---
```python
"""
Iterate through each row of the input grid. For each row, change the color of the leftmost pixel to blue. Leave all other pixels in the grid unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each row and change the leftmost pixel to blue (1)
    for i in range(output_grid.shape[0]):
        output_grid[i, 0] = 1

    return output_grid
```

