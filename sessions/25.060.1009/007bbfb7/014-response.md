# 007bbfb7 • 014 • refine_coder

---
```python
"""
Expand a 3x3 input grid to a 9x9 output grid, replicating yellow (4) pixels based on their row in the input:
- Row 0: Replicated at (0, j) and (0, j+6) in the output.
- Row 2: Replicated at (2, j), (6, j+3), and (8, j+3) in the output.
- Row 1: Not replicated.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 9x9 array filled with white (0)
    output_grid = np.zeros((9, 9), dtype=int)

    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # Iterate through the input grid to find and replicate yellow pixels
    for i in range(input_height):
        for j in range(input_width):
            if input_grid[i, j] == 4:
                # Top Row (Row 0) Replication
                if i == 0:
                    output_grid[0, j] = 4
                    output_grid[0, j + 6] = 4
                # Bottom Row (Row 2) Replication
                elif i == 2:
                    output_grid[2, j] = 4
                    output_grid[6, j + 3] = 4
                    output_grid[8, j + 3] = 4
                # Row 1 is ignored

    return output_grid
```

