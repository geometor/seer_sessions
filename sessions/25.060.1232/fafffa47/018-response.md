# fafffa47 • 018 • refine_coder

---
```python
"""
The input grid is reduced to half its height, maintaining the same width.
Any maroon(9) pixels in the top half of the input are transformed to red(2)
pixels in the output, with their positions horizontally mirrored within their
respective rows. Any blue(1) pixels in the input are transformed to red(2)
pixels at the same relative location in the output grid, but at the reduced
output dimensions. All white(0) pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid
    input_height, input_width = input_grid.shape
    output_height = input_height // 2
    output_width = input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Color Transformation (Top Half)
    for i in range(output_height):
        for j in range(input_width):
            if input_grid[i, j] == 9:
                output_grid[i, input_width - 1 - j] = 2

    # Color Transformation (Blue(1) to Red(2)) - All of Input
    for i in range(input_height):
        for j in range(input_width):
          if input_grid[i, j] == 1:
              # Map input row index to output row index
              output_row = i % output_height
              output_grid[output_row,j] = 2

    # White Retention (Implicit, as we initialize with 0)

    return output_grid
```
