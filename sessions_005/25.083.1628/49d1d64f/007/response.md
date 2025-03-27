```python
"""
Transforms the input grid by duplicating each pixel into a 2x2 block and adding a black border.

1. Initialization: Create an output grid filled with black pixels (0). The
   height of the output grid is the height of the input grid plus 2. The width
   of the output grid is twice the width of the input grid plus 2.

2. Pixel Duplication: For each pixel in the input grid, copy its value to a 2x2
   block of pixels in the output grid. The top-left corner of this 2x2 block
   starts at the row and column indices in the *output grid* given by
   (row_input * 1 + 1 , col_input * 2 + 1).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height + 2
    output_width = input_width * 2 + 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Duplicate pixels and add black border
    for row in range(input_height):
        for col in range(input_width):
            # Map input pixel to a 2x2 block in the output grid
            output_grid[row + 1, 2 * col + 1] = input_grid[row, col]
            output_grid[row + 1, 2 * col + 2] = input_grid[row, col]
            output_grid[row + 2, 2 * col + 1] = input_grid[row, col]
            output_grid[row + 2, 2 * col + 2] = input_grid[row, col]
    return output_grid
```