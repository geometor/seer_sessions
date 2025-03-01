# 6773b310 • 026 • refine_coder

---
```python
"""
Transforms an input grid by finding a single azure (8) pixel and placing a blue (1) pixel at the same location in an output grid of the same dimensions. All other pixels in the output grid are set to black (0).
"""

import numpy as np

def transform(input_grid):
    # Create an output grid with matching dimensions of input.
    output_grid = np.zeros_like(input_grid, dtype=int)

    # Find the coordinates (row, column) of *any single* azure (8) pixel.
    azure_pixels = np.where(np.array(input_grid) == 8)
    if azure_pixels[0].size > 0:  # Check if any azure pixels were found
        row = azure_pixels[0][0]
        col = azure_pixels[1][0]

        # Place a blue pixel at the same location.
        output_grid[row, col] = 1

    return output_grid.tolist()
```
