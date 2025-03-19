# f76d97a5 • 008 • example_2 • investigate_coder

---
```python
"""
Replaces all gray (5) pixels in the input grid with white (0) pixels, while keeping magenta (6) pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing gray pixels with white pixels, leaving magenta pixels unchanged.
    """
    # Create a copy of the input grid to serve as the output grid.  We modify the copy.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the grid
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is gray (5)
            if output_grid[i, j] == 5:
                # Replace gray pixels with white (0)
                output_grid[i, j] = 0

    return output_grid
```
