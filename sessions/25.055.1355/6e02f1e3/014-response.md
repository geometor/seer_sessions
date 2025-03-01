# 6e02f1e3 • 014 • example_3 • investigate_coder

---
```python
"""
Transforms a 3x3 input grid filled with yellow (4) pixels into a 3x3 output grid where the first row is gray (5) and the remaining two rows are white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.  This ensures
    # it's the same size and type.
    output_grid = np.copy(input_grid)

    # Change the color of the first row to gray (5).
    output_grid[0, :] = 5

    # Change the color of the second and third rows to white (0).
    output_grid[1:, :] = 0

    return output_grid
```
