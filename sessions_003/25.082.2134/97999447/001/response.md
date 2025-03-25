```python
"""
Iterates through each row of the input grid. If a row contains exactly one non-zero pixel,
it expands that pixel horizontally to the right, inserting a gray pixel (5) between each expansion.
Rows that do not meet this condition remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the horizontal expansion rule."""
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of the input
    rows, cols = output_grid.shape

    for r in range(rows):
        # Find non-zero pixels in the current row
        non_zero_pixels = np.where(output_grid[r] != 0)[0]

        # If there is exactly one non-zero pixel
        if len(non_zero_pixels) == 1:
            c = non_zero_pixels[0]
            original_color = output_grid[r, c]

            # Expand the pixel horizontally and insert gray pixels
            for i in range(c, cols):
                if (i-c)%2 == 0:
                    output_grid[r, i] = original_color
                else:
                    output_grid[r,i] = 5

    return output_grid
```
