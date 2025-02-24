# 5582e5ca • 014 • example_3 • investigate_coder

---
```python
"""
1. **Identify the Target Color:** Examine the input grid and find the color magenta (represented by the value 6).
2. **Flood Fill:** Create a new grid (output grid) of the same dimensions as the input grid. Fill the output grid entirely with color 6 (magenta).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by flooding it with magenta (6)."""

    # Initialize the output grid with the same dimensions as the input.
    output_grid = np.full(input_grid.shape, 6)

    return output_grid
```
