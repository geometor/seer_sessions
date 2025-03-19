# 9565186b • 012 • refine_coder

---
```python
"""
Identify all pixels that are not blue. Change the color of these non-blue pixels to gray. Keep the blue pixels unchanged.
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
    # Initialize the output grid with the same dimensions and values as the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel in the input grid.
    for row_index in range(output_grid.shape[0]):
        for col_index in range(output_grid.shape[1]):
            # Check if the pixel's color is not blue (1).
            if output_grid[row_index, col_index] != 1:
                # Change the pixel's color to gray (5).
                output_grid[row_index, col_index] = 5

    return output_grid
```

