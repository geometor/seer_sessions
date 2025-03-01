# 05269061 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to expand a 3x1 pattern of red (2), azure (8), and green (3) pixels from the top-left corner into a checkerboard pattern across the entire grid, replacing all white (0) pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding a 3x1 pattern into a checkerboard.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    pattern = [2, 8, 3]

    # Iterate through the output grid and apply the checkerboard pattern.
    for i in range(rows):
        for j in range(cols):
            output_grid[i, j] = pattern[(i + j) % 3]  # Use modulo operator
    return output_grid
```
