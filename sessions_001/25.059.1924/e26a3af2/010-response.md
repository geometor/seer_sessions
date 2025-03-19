# e26a3af2 • 010 • example_2 • investigate_coder

---
```python
"""
Iterate through the input grid. Keep the pixel in the output grid at the same position only if its color is blue (1), red (2), or azure (8). Other colors are discarded.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.zeros_like(input_grid)

    # Iterate through each cell of the input grid.
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_color in enumerate(row):
            # Check if the pixel's color should be kept.
            if pixel_color in [1, 2, 8]:
                output_grid[row_index, col_index] = pixel_color

    return output_grid
```
