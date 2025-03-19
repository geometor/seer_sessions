# d037b0a7 • 016 • refine_coder

---
```python
"""
1. Identify the top-left pixel: Find the color of the pixel at position (0, 0) of the input grid.
2. Replicate the top-left pixel downwards: Fill the entire first column (column 0) of the output grid with the color identified in step 1.
3. Identify the center pixel: Find the color of the pixel at the center (1,1) of the input grid.
4. Replicate center pixel downwards once: In the output grid, set the color of the pixel at position that is one row below the center pixel's row, and in the same column to the color found in step 3.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # 1. Identify and replicate the top-left pixel downwards
    top_left_color = input_grid[0, 0]
    for row in range(output_grid.shape[0]):
        output_grid[row, 0] = top_left_color

    # 2. Identify the center pixel and replicate down once.
    center_color = input_grid[1, 1]
    if 1+1 < output_grid.shape[0]: # check not outside bounds
      output_grid[1 + 1, 1] = center_color

    return output_grid
```

