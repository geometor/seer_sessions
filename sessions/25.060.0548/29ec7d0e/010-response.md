# 29ec7d0e • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to replace all white (0) pixels in the input grid with blue (1) pixels, while keeping all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all white pixels (0) with blue pixels (1).

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of all white pixels (where the value is 0).
    white_pixels = np.where(output_grid == 0)

    # Replace the color of the identified white pixels with blue (1).
    output_grid[white_pixels] = 1

    return output_grid
```
