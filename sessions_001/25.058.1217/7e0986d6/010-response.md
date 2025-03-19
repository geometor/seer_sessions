# 7e0986d6 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation removes all blue (1) pixels from the input grid, changing them to grey (0).
"""

import numpy as np

def transform(input_grid):
    """
    Removes all blue pixels from the input grid.

    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.

    Returns:
        numpy.ndarray: The modified grid with blue pixels removed.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of all blue pixels (where the value is 1).
    blue_pixel_coords = np.where(output_grid == 1)

    # Change the color of blue pixels to grey (0) in the output grid.
    output_grid[blue_pixel_coords] = 0

    return output_grid
```
