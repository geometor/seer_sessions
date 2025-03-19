# 6e02f1e3 • 016 • refine_coder

---
```python
"""
Transforms an input grid of any size and color composition into an output grid of the same size, where the first row is changed to gray (5) and all subsequent rows are changed to white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid to maintain dimensions.
    output_grid = np.copy(input_grid)

    # Set the first row to gray (5).
    output_grid[0, :] = 5

    # Set all rows from the second row onwards to white (0).
    output_grid[1:, :] = 0

    return output_grid
```

