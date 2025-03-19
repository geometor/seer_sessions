# 5582e5ca • 002 • example_1 • investigate_coder

---
```python
"""
Identifies the color '4' (yellow) within the input grid and creates an output grid of the same dimensions, filled entirely with '4' (yellow).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all cells with the value 4.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array of the same dimensions as the input_grid, with all cells set to 4.
    """
    # Initialize output_grid with the same dimensions as input_grid.
    output_grid = np.full(input_grid.shape, 4)

    # No need for further modification since the grid is already filled with 4.

    return output_grid
```
