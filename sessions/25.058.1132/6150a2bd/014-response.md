# 6150a2bd • 014 • refine_coder

---
```python
"""
The input grid is transformed into the output grid by performing a vertical flip (top-to-bottom mirror). This is achieved by swapping the positions of rows. The first row of the input becomes the last row of the output, the second row of the input becomes the second-to-last row of the output, and so on. The operation effectively inverts the vertical order of the rows while preserving the horizontal order of pixels within each row.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    n = output_grid.shape[0]

    # Iterate through rows up to the midpoint.
    for i in range(n // 2):
        # Swap row i with row n-1-i.
        output_grid[[i, n - 1 - i]] = output_grid[[n - 1 - i, i]]

    return output_grid
```

