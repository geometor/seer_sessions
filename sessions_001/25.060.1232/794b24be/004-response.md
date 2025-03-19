# 794b24be • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is: Find the single non-zero pixel in the input grid. Move this pixel to the top-left corner of the grid (position (0, 0)). Change the color of this pixel to red (value 2). Set all other pixels in the grid to white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Initialize the output grid as a copy of the input grid, but filled with 0s (white).
    output_grid = np.zeros_like(input_grid)

    # Find the coordinates of the non-zero pixel.
    non_zero_indices = np.nonzero(input_grid)
    if len(non_zero_indices[0]) > 0:  # Check if there is at least one non-zero pixel
      # non_zero_row, non_zero_col = non_zero_indices[0][0], non_zero_indices[1][0] # this is not needed

      # Move the pixel to the top-left corner (0, 0) and change its color to red (2).
      output_grid[0, 0] = 2

    return output_grid
```
