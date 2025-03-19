# 49d1d64f • 005 • refine_coder

---
```python
"""
1.  **Initialization:** Create an output grid filled with zeros (white). The dimensions of this grid depend on the input grid.
2.  **Expansion:** For each pixel in the input grid:
    *   Create a 1x1 region of the same color and value in the corresponding section of the output grid
    *   Pad the region by surrounding the value on all sides with zeros.
    *   If the input is a single pixel, the output is 3x3 and the single pixel is centered.
    *   If the input grid has dimensions *m* x *n*, the output grid should have the dimensions  (*m* + 2) x (*n* + 2)

3. **Output:** Return the output.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the padding rule."""

    input_rows, input_cols = input_grid.shape
    output_rows = input_rows + 2
    output_cols = input_cols + 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through input pixels and place them in the output grid
    for i in range(input_rows):
        for j in range(input_cols):
            output_grid[i + 1, j + 1] = input_grid[i, j]

    return output_grid
```
