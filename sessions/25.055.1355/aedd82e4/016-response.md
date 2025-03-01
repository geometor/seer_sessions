# aedd82e4 • 016 • refine_coder

---
```python
"""
Find the red pixel at row 3, last column and change it's color to blue.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    # change output pixels
    #check if row 3 and last column exists
    if rows > 2 and cols > 0:
        # change the color of the pixel at row 3, last column from red(2) to blue (1)
        if output_grid[2, cols -1] == 2:
           output_grid[2, cols - 1] = 1

    return output_grid
```

