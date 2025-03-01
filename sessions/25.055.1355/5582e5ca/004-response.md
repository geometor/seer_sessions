# 5582e5ca • 004 • refine_coder

---
```python
"""
The transformation rule is to identify the last non-zero color present in the input grid, reading from top-left to bottom-right, and create an output grid of the same dimensions where all pixels are of that color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid into an output grid of the same dimensions,
    where all pixels in the output grid have the last non-zero color value
    found in the input grid (reading left-to-right, top-to-bottom)
    """
    # Initialize output_grid with the same dimensions as the input_grid
    output_grid = np.zeros_like(input_grid)

    # Find the last non-zero color
    target_color = 0
    for row in input_grid:
        for pixel in row:
            if pixel != 0:
                target_color = pixel

    # Fill the output_grid with the target color
    output_grid[:] = target_color

    return output_grid
```
