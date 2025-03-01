# 484b58aa • 012 • example_3 • investigate_coder

---
```python
"""
The transformation rule is to remove all pixels of color 0 (white) from the input grid, preserving the remaining pixels in their original positions within the grid structure.
"""

import numpy as np

def transform(input_grid):
    """
    Removes all pixels of color 0 (white) from the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid with white pixels removed.
    """
    # Create an output grid of the same dimensions filled.
    output_grid = np.copy(input_grid)

    # Iterate through each cell and remove the background color.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 0:
                output_grid[i,j] = 0 # explicitly assign 0 to maintain original grid

    return output_grid
```
