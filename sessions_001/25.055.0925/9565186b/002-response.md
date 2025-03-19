# 9565186b • 002 • example_1 • investigate_coder

---
```python
"""
Preserve Red: Keep all pixels with the value 2 (red) unchanged.
Recolor to Grey: Change all pixels that have the value 1 (blue) or 8 (azure) to 5 (grey).
Grid structure: The input grid dimensions must equal output grid dimensions.
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid according to color rules."""

    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Apply color transformation rules
            if output_grid[i, j] == 1 or output_grid[i, j] == 8:
                output_grid[i, j] = 5

    return output_grid
```

