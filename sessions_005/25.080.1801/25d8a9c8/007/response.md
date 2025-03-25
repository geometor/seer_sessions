```python
"""
Transforms an input grid by checking if all cells within each row have the same color. If they do, the row is filled with 5; otherwise, it's filled with 0.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid based on the uniformity of colors within each row.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.zeros_like(input_grid)

    for i, row in enumerate(input_grid):
        # Check if all elements in the row are the same
        if np.all(row == row[0]):
            output_grid[i, :] = 5  # Fill the entire row with 5
        else:
            output_grid[i, :] = 0  # Fill the entire row with 0

    return output_grid
```
