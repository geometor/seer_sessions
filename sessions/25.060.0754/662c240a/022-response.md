# 662c240a • 022 • refine_coder

---
```python
"""
Extracts the bottom-right 3x3 subgrid from the input grid, preserving only
those colors that were present in the original input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the bottom-right 3x3 subgrid and filters colors.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The bottom-right 3x3 subgrid with color filtering.
    """
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Calculate the starting row and column indices for the 3x3 subgrid.
    start_row = rows - 3
    start_col = cols - 3

    # Handle cases where the input grid is smaller than 3x3.
    if start_row < 0 or start_col < 0:
        return np.zeros((3,3), dtype=int) # Return a black 3x3 grid

    # Extract the 3x3 subgrid.
    output_grid = input_grid[start_row:rows, start_col:cols].copy()

    # Get the unique colors in the input grid.
    input_colors = np.unique(input_grid)

    # Filter the colors in the output grid.
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if output_grid[r, c] not in input_colors:
                output_grid[r, c] = 0  # Set to black if not in input colors

    return output_grid
```

