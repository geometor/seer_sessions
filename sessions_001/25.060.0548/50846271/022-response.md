# 50846271 • 022 • refine_coder

---
```python
"""
Identify red (2) pixels in the input grid. Replace the leftmost red pixels in each row with azure (8) pixels. The rest of the grid (gray (5) and white (0) pixels) remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing the leftmost red pixels in each row with azure pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of all red pixels.
    red_pixels = np.argwhere(input_grid == 2)

    # Iterate through each row.
    for row in range(output_grid.shape[0]):
        # Find red pixels in the current row.
        red_in_row = [pixel for pixel in red_pixels if pixel[0] == row]

        # If there are red pixels in the row, find the leftmost one.
        if red_in_row:
            leftmost_red = min(red_in_row, key=lambda x: x[1])

            # Replace the leftmost red pixel with azure.
            output_grid[leftmost_red[0], leftmost_red[1]] = 8

    return output_grid
```
