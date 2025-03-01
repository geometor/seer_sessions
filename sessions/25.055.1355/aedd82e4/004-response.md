# aedd82e4 • 004 • refine_coder

---
```python
"""
The output grid is identical to the input grid, except for the bottom-left corner pixel. The color of the bottom-left pixel in the output grid is always blue, regardless of its original color in the input grid. All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Change the color of the pixel in the bottom-left corner to blue (1)
    output_grid[output_grid.shape[0] - 1, 0] = 1

    return output_grid
```

