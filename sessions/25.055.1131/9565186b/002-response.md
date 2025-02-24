# 9565186b • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to replace all non-red pixels with gray, while leaving the red pixels untouched.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all non-red pixels with gray.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Get the dimensions of the grid.
    rows, cols = output_grid.shape

    # Iterate over all pixels.
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is not red (2).
            if output_grid[i, j] != 2:
                # Replace the pixel with gray (5).
                output_grid[i, j] = 5

    return output_grid
```

