# 794b24be • 006 • refine_coder

---
```python
"""
The transformation rule is as follows:

1.  Examine the input grid.
2.  If there are any non-zero pixels in the input grid:
    *   Create an output grid of the same dimensions, filled entirely with white (0) pixels.
    *   Place a single red (2) pixel in the top-left corner (0, 0) of the output grid.
3.  If there are NO non-zero pixels in the input grid:
    *   The output grid is identical to the input grid (all white/0).

Essentially, regardless of *how many* non-zero pixels are present, or their original colors, the output *always* has a single red pixel at (0,0) if *any* non-zero pixels existed, and is all white otherwise. The original color and location of the input non-zero pixel(s) are irrelevant.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Initialize the output grid as a copy of the input grid, but filled with 0s (white).
    output_grid = np.zeros_like(input_grid)

    # Check if there are any non-zero pixels in the input grid.
    if np.any(input_grid):
        # If any non-zero pixels exist, set the top-left pixel to red (2).
        output_grid[0, 0] = 2

    return output_grid
```

