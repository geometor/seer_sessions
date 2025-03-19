# 97999447 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is: For each non-zero pixel in the input grid, extend it horizontally to the right with gray (5) pixels until the end of the row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    For each non-zero pixel, extend it to the right with gray (5) pixels.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the grid.
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is non-zero.
            if output_grid[r, c] != 0:
                # Extend to the right with gray pixels.
                for c2 in range(c + 1, cols):
                    output_grid[r, c2] = 5
    return output_grid
```
