# 9565186b • 020 • example_4 • investigate_coder

---
```python
"""
Iterate through each pixel of the input grid. If the pixel is yellow (4), keep it yellow. Otherwise, change the pixel to gray (5).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing all non-yellow pixels to gray.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate over each cell
    for i in range(rows):
        for j in range(cols):
           # change to gray if not yellow
           if output_grid[i,j] != 4:
               output_grid[i,j] = 5

    return output_grid
```
