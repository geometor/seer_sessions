# 94f9d214 • 016 • example_3 • investigate_coder

---
```python
"""
The input grid is processed in 2x1 blocks. If a 2x1 block contains the color green (3), the corresponding output cell is red (2). Otherwise, the output cell is white (0). The output grid is 4x4.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through 2x1 blocks
    for i in range(4):
        for j in range(4):
            # Extract 2x1 block
            block = input_grid[2*i:2*i+2, j]

            # Check for green (3) in the block
            if 3 in block:
                output_grid[i, j] = 2  # Set to red
            else:
                output_grid[i, j] = 0  # Set to white

    return output_grid
```
