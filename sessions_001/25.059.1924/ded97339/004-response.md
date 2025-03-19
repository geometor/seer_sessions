# ded97339 • 004 • example_1 • investigate_coder

---
```python
"""
Identify all azure (8) pixels in the input grid. For each azure pixel, create a vertical strip of azure pixels in the output grid, starting from the azure pixel's row and extending downwards. All other pixels in the output grid remain white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid, then we modify.
    output_grid = np.copy(input_grid)

    # Iterate through all pixels in the input grid.
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_value in enumerate(row):
            # Check if the pixel is azure (8).
            if pixel_value == 8:
                # Create a vertical strip downwards.
                for r in range(row_index, len(input_grid)):
                    output_grid[r][col_index] = 8

    return output_grid
```
