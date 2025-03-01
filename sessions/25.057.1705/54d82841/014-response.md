# 54d82841 • 014 • example_3 • investigate_coder

---
```python
"""
Adds a row at the bottom of the grid. The new row contains yellow (4) pixels in columns where the original input columns contained only white (0) pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Add a new row of zeros to the bottom of the grid
    new_row = np.zeros((1, output_grid.shape[1]), dtype=int)
    output_grid = np.vstack((output_grid, new_row))

    # Iterate through each column of the *original* input grid
    for j in range(input_grid.shape[1]):
        # Check if all pixels in the column are white (0)
        if np.all(input_grid[:, j] == 0):
            # Set the corresponding pixel in the new row to yellow (4)
            output_grid[-1, j] = 4

    return output_grid
```
