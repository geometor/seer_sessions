# 2dee498d • 002 • example_1 • investigate_coder

---
```python
"""
The transformation extracts every third column from the input grid, starting with the first column, and uses those to create a new, smaller grid. The row count does not change.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols // 3), dtype=int)

    # change output pixels
    new_col_index = 0
    for j in range(0, cols, 3):
        output_grid[:, new_col_index] = input_grid[:, j]
        new_col_index += 1

    return output_grid.tolist()
```
