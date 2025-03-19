# 73251a56 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to remove all white (0) pixels from the input grid while preserving the positions of all other colored pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Removes all white (0) pixels from the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid with white pixels removed.
    """
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)

    # Iterate through the grid and replace white pixels with the surrounding color
    rows, cols = output_grid.shape
    for i in range(rows):
        for j in range(cols):
            if output_grid[i, j] == 0:
               output_grid[i,j] = 5 #set to 5 (grey)

    return output_grid
```

