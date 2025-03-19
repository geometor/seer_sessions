# 7447852a • 014 • example_3 • investigate_coder

---
```python
"""
Iterates through the input grid, identifies red (2) pixels, and checks their immediate horizontal neighbors.
If a neighbor is white (0), it's replaced with yellow (4) in the output grid.
All original red (2) pixels are copied to output unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output grid as a copy of input

    rows, cols = input_grid.shape

    # Iterate through each cell
    for i in range(rows):
        for j in range(cols):
            # Check for red pixels
            if input_grid[i, j] == 2:
                # Check left neighbor
                if j > 0 and input_grid[i, j - 1] == 0:
                    output_grid[i, j - 1] = 4
                # Check right neighbor
                if j < cols - 1 and input_grid[i, j + 1] == 0:
                    output_grid[i, j + 1] = 4

    return output_grid
```

