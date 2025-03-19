# 49d1d64f • 006 • refine_coder

---
```python
"""
Expands each pixel of the input grid into a 2x2 block in the output grid,
and fills the borders (top and bottom rows, leftmost and rightmost columns) with 0.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid. Add 2 to height and width for the border.
    input_height, input_width = input_grid.shape
    output_height = input_height * 2 + 2
    output_width = input_width * 2 + 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels 
    # expansion:  Iterate through the input and expand to 2x2 blocks in the output.
    for row in range(input_height):
        for col in range(input_width):
            output_grid[row*2 + 1, col*2 + 1] = input_grid[row, col]
            output_grid[row*2 + 1, col*2 + 2] = input_grid[row, col]
            output_grid[row*2 + 2, col*2 + 1] = input_grid[row, col]
            output_grid[row*2 + 2, col*2 + 2] = input_grid[row, col]

    return output_grid
```

