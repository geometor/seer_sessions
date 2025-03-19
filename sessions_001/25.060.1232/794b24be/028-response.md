# 794b24be • 028 • refine_coder

---
```python
"""
The transformation rule is as follows:
1.  Identify Non-zero Pixels: Examine the input grid and find all pixels with a non-zero value (representing any color other than white).
2.  Output Grid Initialization: Create an output grid of the same dimensions as the input grid, filled entirely with zeros (white).
3.  Place Red Pixel: Regardless of how many non-zero pixels there are in the input, or what color the non-zero pixel are, place a single red pixel (value 2) at the top-left corner (position [0, 0]) of the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros, same size as input
    output_grid = np.zeros_like(input_grid)

    # Place a red pixel (value 2) at the top-left corner (0,0)
    output_grid[0, 0] = 2

    return output_grid
```

