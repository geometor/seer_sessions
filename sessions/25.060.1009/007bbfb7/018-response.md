# 007bbfb7 • 018 • example_3 • investigate_coder

---
```python
"""
The input grid (3x3) is expanded to a 9x9 grid. Each pixel in the input grid is transformed into a 3x3 block in the output grid. If a cell is a red(value = 2) pixel, it gets expanded and all of it's block will be red(value=2). All other area are filled by white cells(value=0)
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
            # Replicate each pixel to a 3x3 block
            value = input_grid[i, j]
            for row_offset in range(3):
                for col_offset in range(3):
                    output_grid[i * 3 + row_offset, j * 3 + col_offset] = value

    return output_grid
```
