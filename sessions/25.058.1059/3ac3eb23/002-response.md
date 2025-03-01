# 3ac3eb23 • 002 • example_2 • investigate_coder

---
```python
"""
Transforms an input grid by replicating non-zero pixels vertically in an alternating pattern.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replicating and alternating non-zero pixels.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Iterate through the input grid
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            # Identify non-zero pixels
            if input_grid[r, c] != 0:
                # Replicate the pixel's color in the output grid
                output_grid[r, c] = input_grid[r, c]
                # Alternate replication down the column
                for i in range(r + 1, rows):
                    if (i - r) % 2 != 0:
                      output_grid[i,c] = input_grid[r,c]

    return output_grid.tolist()
```
