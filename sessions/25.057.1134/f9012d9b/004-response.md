# f9012d9b • 004 • refine_coder

---
```python
"""
Extract the top-left 2x2 subgrid from the input grid, regardless of the input's dimensions.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the top-left 2x2 subgrid from the input grid.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The 2x2 subgrid.
    """
    # The output grid is always 2x2.
    output_grid = np.zeros((2, 2), dtype=int)

    # Iterate through the top-left 2x2 region of the input grid.
    #  Handle cases where input grid is smaller than 2x2.
    for i in range(min(2, input_grid.shape[0])):
        for j in range(min(2, input_grid.shape[1])):
            output_grid[i, j] = input_grid[i, j]

    return output_grid
```

