# 007bbfb7 • 020 • refine_coder

---
```python
"""
The input grid is expanded into a larger grid where each original pixel becomes a 3x3 block. The color of each 3x3 block in the output grid is the same as the color of the corresponding pixel in the input grid. For example, if a pixel in the input grid is blue, the corresponding 3x3 block in the output grid will be entirely blue. If a pixel is white, its 3x3 block will be white. This applies to all colors and pixels in the input grid.
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

