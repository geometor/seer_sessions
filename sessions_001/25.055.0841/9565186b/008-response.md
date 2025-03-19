# 9565186b • 008 • example_2 • investigate_coder

---
```python
"""
Replace all non-blue pixels with gray pixels, preserving the position of all pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all non-blue pixels with gray pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel in the input grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the pixel's color is not blue (1).
            if output_grid[i, j] != 1:
                # Change the pixel's color to gray (5).
                output_grid[i, j] = 5

    return output_grid
```
