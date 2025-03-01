# 05269061 • 011 • refine_coder

---
```python
"""
Transforms an input grid based on a color mapping that depends on the original color of the pixel and its original index within the set of blue pixels. White pixels remain unchanged.

1.  Iterate through each pixel in the input grid.
2.  Determine the original color of the pixel.
3.  Apply a color transformation based on the following rules:
    - Input Blue at index 0 -> Output Yellow
    - Input Blue at index 1 -> Output Red
    - Input Blue at index 2 -> Output Blue
    - Input White -> No change
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified color mapping rules.
    """
    output_grid = np.copy(input_grid)  # Start with a copy of the input
    rows, cols = input_grid.shape
    blue_indices = []

    # Find the indices of all blue pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:
                blue_indices.append((r, c))

    # Apply color transformation based on the blue pixel's index
    for i, (r, c) in enumerate(blue_indices):
        if i == 0:
            output_grid[r, c] = 4  # Yellow
        elif i == 1:
            output_grid[r, c] = 2  # Red
        elif i == 2:
            output_grid[r,c] = 1 # Blue

    return output_grid
```
