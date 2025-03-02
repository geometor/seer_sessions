# b91ae062 • 014 • refine_coder

---
```python
"""
The transformation rule takes each pixel in the input grid and expands it into a 2x2 block of pixels in the output grid. The color of the original pixel is preserved in the expanded 2x2 block.  The output grid is therefore twice as tall and twice as wide as the input grid. The top-left corner of each 2x2 block in the output corresponds to the original pixel's location (row, col) multiplied by two, i.e., (2*row, 2*col).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = 2 * input_height, 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    for row in range(input_height):
        for col in range(input_width):
            # Get the color of the current input pixel
            color = input_grid[row, col]
            # Expand the pixel to a 2x2 block in the output grid
            output_grid[2*row:2*row+2, 2*col:2*col+2] = color

    return output_grid
```

