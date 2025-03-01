# d037b0a7 • 010 • refine_coder

---
```python
"""
Copies the second row of the input grid to the last row of the output grid, keeping all other rows unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a grid by copying the second row of the input to the last row of the output.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Copy the second row (index 1) to the last row (index -1).
    output_grid[-1, :] = input_grid[1, :]

    return output_grid
```

