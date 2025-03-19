# db3e9e38 • 008 • refine_coder

---
```python
"""
1.  **Identify Orange Pixels:** Locate all pixels with the color orange (7) within the input grid.
2.  **Adjacent Pixel Transformation:** For each orange pixel:
    *   Check for adjacent pixels directly above, below, to the left, and to the right.
    *   If an adjacent pixel exists, change its color to azure (8).
    *   Diagonal neighbors are not affected.
3. **Preserve Original Orange**: The orange pixels that initiate the transformation should remain orange.
"""

import numpy as np

def get_orange_pixels(grid):
    """Finds the coordinates of all orange (7) pixels in the grid."""
    orange_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 7:
                orange_pixels.append((row_index, col_index))
    return orange_pixels

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Get the coordinates of orange pixels
    orange_pixels = get_orange_pixels(input_grid)

    # Iterate through orange pixels and change surrounding colors
    for row, col in orange_pixels:
        # Change above
        if row > 0:
            output_grid[row - 1, col] = 8
        # Change below
        if row < rows - 1:
            output_grid[row + 1, col] = 8
        # Change left
        if col > 0:
            output_grid[row, col - 1] = 8
        # Change right
        if col < cols - 1:
            output_grid[row, col + 1] = 8

    return output_grid
```

