# 2dee498d • 020 • refine_coder

---
```python
"""
The transformation rule extracts the first two columns of the input grid. The output grid has a width of 2 and the same height as the input. The values in the output are the same as the first two columns.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same number of rows as the input and 2 columns.
    output_grid = np.empty((input_grid.shape[0], 2), dtype=int)

    # Copy the first two columns from the input grid to the output grid.
    output_grid[:, 0] = input_grid[:, 0]
    output_grid[:, 1] = input_grid[:, 1]

    return output_grid
```

