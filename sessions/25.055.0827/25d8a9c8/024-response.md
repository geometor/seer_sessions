# 25d8a9c8 • 024 • refine_coder

---
```python
"""
The transformation rule is: Change all pixels in the bottom row to gray, while keeping all other pixels in the grid unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Change all pixels in the bottom row to gray, keeping all other pixels unchanged.
    """
    # Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Get the height of the grid.
    height = output_grid.shape[0]

    # Set the bottom row to gray (5).
    output_grid[height-1, :] = 5

    return output_grid
```

