# e179c5f4 • 011 • refine_coder

---
```python
"""
Generates a checkerboard pattern of 1s (blue) and 8s (azure) based on the dimensions of the input grid. The input grid itself is ignored, only its dimensions are used.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into a checkerboard pattern of 1s and 8s.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array with the same dimensions as the input grid,
        filled with a checkerboard pattern of 1s and 8s.
    """
    # Get Dimensions
    height, width = input_grid.shape

    # Create Output Grid
    output_grid = np.zeros((height, width), dtype=int)

    # Generate Checkerboard
    for row in range(height):
        for col in range(width):
            # Assign Values based on (row + column) % 2
            if (row + col) % 2 == 0:
                output_grid[row, col] = 1  # Blue
            else:
                output_grid[row, col] = 8  # Azure

    return output_grid
```

