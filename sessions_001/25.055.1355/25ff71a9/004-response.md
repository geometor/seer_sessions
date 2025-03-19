# 25ff71a9 • 004 • refine_coder

---
```python
"""
The transformation rule is a cyclic permutation of rows. All rows are moved downwards, and the last row wraps around to become the first row. The presence of a blue row is not a determining factor; the operation is applied regardless.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Shift the rows down by one (cyclic permutation)
    output_grid = np.roll(input_grid, shift=1, axis=0) #roll rows down by 1

    return output_grid
```
