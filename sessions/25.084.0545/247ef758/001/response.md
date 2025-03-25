```python
"""
Transforms an input grid by propagating the first non-zero pixel's color in each row and column, replacing '0' pixels. The propagation stops when it encounters a different non-zero pixel or the grid boundary.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Propagate colors in rows (left to right)
    for i in range(rows):
        first_non_zero = -1
        for j in range(cols):
            if input_grid[i, j] != 0:
                if first_non_zero == -1:
                    first_non_zero = input_grid[i,j]
            elif first_non_zero != -1:
                output_grid[i,j] = first_non_zero

    # Propagate colors in columns (top to bottom)
    for j in range(cols):
        first_non_zero = -1
        for i in range(rows):
             if input_grid[i, j] != 0:
                if first_non_zero == -1:
                    first_non_zero = input_grid[i,j]
             elif first_non_zero != -1:
                output_grid[i,j] = first_non_zero
    return output_grid
```