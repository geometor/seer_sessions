# 1b2d62fb • 006 • refine_coder

---
```python
"""
1.  **Extract Subgrid:** From the input grid, extract a 3-column wide subgrid. The subgrid starts from the 3rd column (index 2) and extends for 3 columns.

2.  **Replace Color:** Within this subgrid, replace all blue (value 1) pixels with azure (value 8) pixels.

3.  **Conditional Row Modification:** Within the subgrid, identify the row(s) containing azure pixels. For *each* such row, set all pixels that are *not* azure to white (value 0).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    # 1. Extract Subgrid
    output_grid = input_grid[:, 2:5]

    # 2. Replace Color
    output_grid = np.where(output_grid == 1, 8, output_grid)

    # 3. Conditional Row Modification (modify rows based on azure presence)
    azure_rows = np.where(np.any(output_grid == 8, axis=1))[0]
    for row_index in azure_rows:
        for col_index in range(output_grid.shape[1]):
            if output_grid[row_index, col_index] != 8:
                output_grid[row_index, col_index] = 0

    return output_grid
```

