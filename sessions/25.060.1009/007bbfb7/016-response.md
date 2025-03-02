# 007bbfb7 • 016 • refine_coder

---
```python
"""
Transforms a 3x3 input grid into a 9x9 output grid, replicating non-zero pixels
based on their row and color according to specific rules.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 9x9 array filled with white (0)
    output_grid = np.zeros((9, 9), dtype=int)

    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # Iterate through the input grid to find and replicate non-zero pixels
    for i in range(input_height):
        for j in range(input_width):
            pixel_value = input_grid[i, j]
            if pixel_value != 0:
                # Apply replication rules based on row and color
                if i == 0 and pixel_value == 3:  # Row 0, Green
                    output_grid[0, j] = pixel_value
                    output_grid[0, j + 6] = pixel_value
                elif i == 1 and pixel_value == 1:  # Row 1, Blue
                    output_grid[3, j] = pixel_value
                    output_grid[5, j] = pixel_value
                    output_grid[7, j] = pixel_value
                elif i == 2 and pixel_value == 4:  # Row 2, Yellow
                    output_grid[2, j] = pixel_value
                    output_grid[6, j + 3] = pixel_value
                    output_grid[8, j + 3] = pixel_value

    return output_grid
```
