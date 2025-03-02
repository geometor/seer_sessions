# 75b8110e • 014 • refine_coder

---
```python
"""
The input grid is an 8x8 grid, and the output grid is a 4x4 grid. The output grid is a sub-grid of the input grid, created by sampling every other row and every other column of the input grid, starting from the top-left cell (0, 0). All pixel values (including black/0) from the sampled locations are copied to the corresponding locations in the output grid. The relative positions of the pixels are maintained. The output grid includes a direct sample; it does not filter out any color.
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
            
            # Copy the pixel value to output_grid
            output_grid[i, j] = pixel_value
                
    return output_grid
```

