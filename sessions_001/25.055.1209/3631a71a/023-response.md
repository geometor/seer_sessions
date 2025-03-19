# 3631a71a • 023 • refine_coder

---
```python
"""
The task involves transforming a grid of color values.  If the grid contains any pixels
that aren't gray (color 5), those non-gray pixels are changed to gray. If the grid contains only
gray pixels, the output grid should match the input.
"""

import numpy as np

def has_non_gray_pixels(grid):
    """Checks if the grid contains any pixels that are not gray (color 5)."""
    grid = np.array(grid)
    return np.any(grid != 5)

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)  # Start with a copy

    # Check for non-gray pixels
    if has_non_gray_pixels(input_grid):
        # Change all pixels to gray
        output_grid[:] = 5
    
    return output_grid
```
