# 9565186b • 004 • refine_coder

---
```python
"""
The transformation rule is as follows:

1.  Iterate through each pixel in the input grid.
2.  If a pixel is blue (value 1) or azure (value 8), change its color to gray (value 5).
3.  If a pixel is red (value 2), it should not be changed.
4. If a pixel has any color other than blue, azure, and red, do not modify it.
5.  All other pixels in the grid should remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # change output pixels 
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_value in enumerate(row):
            # If a pixel is blue (value 1) or azure (value 8), change its color to gray (value 5).
            if pixel_value == 1 or pixel_value == 8:
                output_grid[row_index, col_index] = 5
            # If a pixel is red (value 2), it should not be changed - implicit, no action needed.
            # all other colors remain unchanged.
    return output_grid
```

