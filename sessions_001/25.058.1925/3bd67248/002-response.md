# 3bd67248 • 002 • example_3 • investigate_coder

---
```python
"""
Transforms an input grid by:
1. Drawing a diagonal line of color '2' (red) from the top-right to the bottom-left.
2. Filling the bottom row with color '4' (yellow).
The transformation is triggered by the presence of a vertical line of a single non-zero color on the left edge of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Create the diagonal line of color 2.
    for i in range(rows):
        output_grid[i, cols - 1 - i] = 2

    # Fill the bottom row with color 4.
    output_grid[rows - 1, :] = 4

    return output_grid
```
