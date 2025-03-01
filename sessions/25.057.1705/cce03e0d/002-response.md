# cce03e0d • 002 • example_1 • investigate_coder

---
```python
"""
The input grid is expanded by a factor of 3 in both dimensions. The original input grid is embedded within the larger output grid, positioned at the start of the second 'band' of 3 rows, on the left edge. The rest of the output grid is filled with white (0) pixels.
"""

import numpy as np

def transform(input_grid):
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 3, input_width * 3

    # Create an output grid filled with white (0).
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Calculate the starting row index for embedding the input grid.
    start_row = output_height // 3
    start_col = 0

    # Embed the input grid into the output grid.
    output_grid[start_row:start_row + input_height, start_col:start_col + input_width] = input_grid

    return output_grid
```
