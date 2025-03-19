# 9565186b • 010 • refine_coder

---
```python
"""
Replace all colors except blue with gray.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel in the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the color is not blue (1)
            if output_grid[i, j] != 1:
                # Replace the color with gray (5)
                output_grid[i, j] = 5

    return output_grid
```

