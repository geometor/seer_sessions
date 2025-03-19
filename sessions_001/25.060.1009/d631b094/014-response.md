# d631b094 • 014 • refine_coder

---
```python
"""
1.  Examine the input grid: Locate all red pixels (pixels with a value of 2). Record their positions.
2.  Transformation Rule:
    *   If red pixels are present: Create a new grid containing *only* the red pixels. The new grid's dimensions will be 1 x N, where N is the number of red pixels found.
    *   If no red pixels are present: The output grid is an exact copy of the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize input_grid as numpy array
    input_grid = np.array(input_grid)
    red_pixels = []

    # find all red pixels using row major traversal
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] == 2:
                red_pixels.append(2)

    # if red pixels exist, create output grid, otherwise, the output is the input
    if len(red_pixels) > 0:
      output_grid = np.array(red_pixels).reshape(1, -1)
    else:
      output_grid = input_grid

    return output_grid.tolist()
```
