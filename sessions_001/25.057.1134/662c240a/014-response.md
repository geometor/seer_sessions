# 662c240a • 014 • example_3 • investigate_coder

---
```python
"""
Extracts the bottom-right 3x3 sub-grid from the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the bottom-right 3x3 sub-grid from the input grid.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The bottom-right 3x3 sub-grid.
    """
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Calculate the starting row and column indices for the 3x3 sub-grid.
    start_row = rows - 3
    start_col = cols - 3

    # Extract the 3x3 sub-grid.
    output_grid = input_grid[start_row:rows, start_col:cols]

    return output_grid
```

