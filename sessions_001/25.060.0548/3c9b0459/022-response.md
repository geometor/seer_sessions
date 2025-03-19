# 3c9b0459 • 022 • example_4 • investigate_coder

---
```python
"""
The transformation rule is a series of swaps between specific cells in the grid:

1. Swap the element at (0, 0) with the element at (2, 0).
2. Swap the element at (0, 1) with the element at (0, 2).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by swapping elements at specific positions.
    """
    output_grid = np.copy(input_grid)

    # Swap (0, 0) with (2, 0)
    output_grid[0, 0], output_grid[2, 0] = output_grid[2, 0], output_grid[0, 0]

    # Swap (0, 1) with (0, 2)
    output_grid[0, 1], output_grid[0, 2] = output_grid[0, 2], output_grid[0, 1]

    return output_grid
```

