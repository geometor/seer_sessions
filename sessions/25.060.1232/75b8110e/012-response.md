# 75b8110e • 012 • refine_coder

---
```python
"""
The input grid is an 8x8 grid, and the output grid is a 4x4 grid. The output grid appears to be a selection, or a sub-grid of the original input grid, and it maintains the relative position of the colored pixels. The output contains all colors that appear in the input, except for 0 (black). All other cells are filled with black (0).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as 4x4 and all black (0)
    output_grid = np.zeros((4, 4), dtype=int)

    input_grid = np.array(input_grid)

    # Iterate over the input grid, checking only the cells
    # that would correspond to the output grid's dimensions.
    for i in range(4):
        for j in range(4):
            # calculate corresponding indices on the input, multiply by 2
            input_row = i * 2
            input_col = j * 2

            # get the pixel value
            pixel_value = input_grid[input_row, input_col]
            
            # if the pixel value is not black (0), copy to output
            if pixel_value != 0:
                output_grid[i, j] = pixel_value
                
    return output_grid
```
