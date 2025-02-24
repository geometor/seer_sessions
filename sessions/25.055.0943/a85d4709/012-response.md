# a85d4709 • 012 • refine_coder

---
```python
"""
The transformation rule keeps pixels with a value of 3 (green) unchanged and changes all other pixels to 3 (green).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # iterate over all pixels in the grid using numpy's ndindex
    for index in np.ndindex(output_grid.shape):
        # if the pixel value is not 3, change it to 3
        if output_grid[index] != 3:
            output_grid[index] = 3

    return output_grid
```
