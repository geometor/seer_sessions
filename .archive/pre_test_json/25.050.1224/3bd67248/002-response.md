# 3bd67248 • 002 • example_1 - CODE

---
```python
"""
The input grid has a magenta (6) vertical line on the leftmost edge. The transformation creates a red (2) diagonal line from the bottom-left to the top-right corner. The bottom row is changed to yellow (4). The rest of the grid remains white (0), except for the first column, which remains magenta.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.zeros_like(input_grid)

    # Keep first column magenta
    output_grid[:, 0] = 6

    # Create a red diagonal
    for i in range(input_grid.shape[0]):
        output_grid[i, input_grid.shape[1] - 1 - i] = 2

    # Make the last row yellow
    output_grid[-1, :] = 4

    return output_grid
```
