# 496994bd • 002 • example_1 • investigate_coder

---
```python
"""
Preserve the top three rows of the input grid.
Preserve the white region.
Mirror the colored region from top to bottom.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Copy the top three rows
    output_grid[:3, :] = input_grid[:3, :]
    
    # Copy the white region.
    output_grid[3:7, :] = input_grid[3:7, :]

    # Mirror the top three rows to the bottom, reversing their order.
    output_grid[7:, :] = input_grid[2::-1, :]
    
    return output_grid.tolist()
```

