# 63613498 • 022 • refine_coder

---
```python
"""
Replaces all non-black (non-zero) pixels in the input grid with grey (5) pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all non-black pixels with grey pixels (5).

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of all non-black pixels (value not 0).
    non_black_pixels = np.where(output_grid != 0)

    # Replace the non-black pixels with grey pixels (value 5).
    output_grid[non_black_pixels] = 5

    return output_grid
```

