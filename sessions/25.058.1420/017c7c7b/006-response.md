# 017c7c7b • 006 • refine_coder

---
```python
"""
Iterates through each pixel in the input grid. Apply the following color changes: White (0) becomes blue (1), blue (1) becomes red (2) and red (2) becomes white(0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by applying a color mapping.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the input grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Apply color mapping: 0->1, 1->2, 2->0
            if output_grid[i, j] == 0:
                output_grid[i, j] = 1
            elif output_grid[i, j] == 1:
                output_grid[i, j] = 2
            elif output_grid[i, j] == 2:
                output_grid[i, j] = 0

    return output_grid
```
