# 017c7c7b • 002 • example_3 • investigate_coder

---
```python
"""
Replaces all blue (1) pixels in the input grid with red (2) pixels, keeping white (0) pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by replacing blue pixels with red pixels.

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
            # If the pixel's color is blue (1), then change it to red (2).
            if output_grid[i, j] == 1:
                output_grid[i, j] = 2
            # Else If the pixel's color is white (0), then it stays white(0).
            elif output_grid[i,j] == 0:
                output_grid[i,j] = 0 # not really necessary, but keep for symmetry

    return output_grid
```

