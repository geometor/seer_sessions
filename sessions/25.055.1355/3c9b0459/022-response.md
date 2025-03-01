# 3c9b0459 • 022 • refine_coder

---
```python
"""
The input grid is transformed into the output grid by swapping the first column with the second column.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Swap the first and second columns
    output_grid[:, 0], output_grid[:, 1] = output_grid[:, 1].copy(), output_grid[:, 0].copy()

    return output_grid
```
