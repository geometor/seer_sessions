# 007bbfb7 • 022 • refine_coder

---
```python
"""
The transformation rule performs a pixel expansion. Each pixel in the input grid is converted into a 3x3 block of pixels in the output grid. The color of each pixel in the input grid is preserved in the corresponding 3x3 block of the output grid. Therefore, the output grid's dimensions are always three times the height and three times the width of the input grid.
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
