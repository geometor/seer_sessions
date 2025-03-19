# 9edfc990 • 008 • refine_coder

---
```python
"""
Identifies '5' (gray) pixels in the input grid and changes them to '1' (blue).  The surrounding '0' (white) pixels are not changed, and no flood-fill behavior is observed. The core rule is a direct replacement of '5' with '1'.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find all instances of '5' (gray) and change them to '1' (blue).
    rows, cols = np.where(output_grid == 5)
    for row, col in zip(rows, cols):
        output_grid[row, col] = 1

    return output_grid
```

