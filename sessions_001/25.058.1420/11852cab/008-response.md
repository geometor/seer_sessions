# 11852cab • 008 • refine_coder

---
```python
"""
Copy the entire input grid to the output grid, then set all pixels in the last row of the output grid to black (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Set all pixels in the last row to black (0).
    output_grid[-1, :] = 0

    return output_grid
```

