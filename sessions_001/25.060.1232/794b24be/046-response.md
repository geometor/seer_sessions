# 794b24be • 046 • refine_coder

---
```python
"""
The transformation rule is as follows:

1.  Identify the top row of the input grid.
2.  Change the color of all pixels in the top row to red.
3. All other pixels not in the top row should stay white.
4.  The output grid is the result of this transformation.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as all white (0) with the same dimensions as the input_grid
    output_grid = np.zeros_like(input_grid)

    # Get the dimensions of the grid
    rows, cols = input_grid.shape

    # Iterate through the columns of the top row (row 0)
    for j in range(cols):
        # Change the color of all pixels in the top row to red (2)
        output_grid[0, j] = 2

    return output_grid
```

