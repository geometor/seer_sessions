# 9172f3a0 • 002 • example_1 • investigate_coder

---
```python
"""
The program takes each pixel in the input grid and expands it into a 3x3 block of the same color in the output grid, maintaining the spatial relationships.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 3, input_cols * 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # change output pixels
    for i in range(input_rows):
        for j in range(input_cols):
            # Expand each pixel to a 3x3 block
            value = input_grid[i, j]
            for row_offset in range(3):
                for col_offset in range(3):
                    output_grid[i*3 + row_offset, j*3 + col_offset] = value

    return output_grid
```
