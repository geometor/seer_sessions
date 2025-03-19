# 67a423a3 • 007 • refine_coder

---
```python
"""
Transforms a grid by changing all white pixels to yellow, while keeping grey pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    - White (0) pixels become yellow (4).
    - Grey (5) pixels remain grey (5).
    - All other pixels remain unchanged.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all pixels.
    for r in range(rows):
        for c in range(cols):
            # Change white pixels to yellow.
            if input_grid[r, c] == 0:
                output_grid[r, c] = 4
            # Grey pixels are unchanged so no action needed.
            # All Other pixels don't need changes

    return output_grid
```
