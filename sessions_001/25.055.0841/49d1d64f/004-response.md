# 49d1d64f • 004 • refine_coder

---
```python
"""
Each pixel in the input grid is expanded into a 2x2 block of the same color in the output grid. There is no added border.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with dimensions 2 * input_height x 2 * input_width
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((2 * input_height, 2 * input_width), dtype=int)

    # iterate through each pixel of the input grid
    for row in range(input_height):
        for col in range(input_width):
            # get the color of the current input pixel
            color = input_grid[row, col]
            
            # calculate the starting position for the 2x2 block in the output grid
            output_row = 2 * row
            output_col = 2 * col
            
            # fill the 2x2 block with the same color
            output_grid[output_row:output_row+2, output_col:output_col+2] = color

    return output_grid
```
