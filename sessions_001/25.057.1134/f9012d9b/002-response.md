# f9012d9b • 002 • example_1 • investigate_coder

---
```python
"""
Extract the top-left 2x2 subgrid from the input grid.
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
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Create an empty output grid.
    output_grid = np.zeros((2, 2), dtype=int)

    # Copy the top-left 2x2 region of the input grid to the output grid.
    for i in range(min(2, rows)):
        for j in range(min(2, cols)):
            output_grid[i, j] = input_grid[i, j]

    return output_grid
```
