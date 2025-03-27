```python
"""
The transformation rule identifies a single blue (1) pixel in the input grid.
It preserves the blue pixel in the output grid.
Then it fills the grid, starting at the blue pixel and alternating azure (8)
and blue (1) in a checkered pattern.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the blue pixel (there should be only one)
    blue_pixels = np.where(input_grid == 1)
    if len(blue_pixels[0]) == 0:
        return output_grid
      
    blue_row, blue_col = blue_pixels[0][0], blue_pixels[1][0]

    # Create checkered pattern
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == (blue_row + blue_col) % 2:
                output_grid[r, c] = 1
            else:
                output_grid[r, c] = 8

    return output_grid
```
