# 46442a0e • 005 • refine_coder

---
```python
"""
The transformation rule takes a 2x2 input grid and expands it into a 4x4 output grid. Each cell in the input grid is replicated to create a 2x2 block in the output grid. The replication is achieved by copying input[i][j] to output[2i][2j], input[i+1][j] to output[2i+1][2j], input[i][j+1] to output[2i][2j+1] and input[i+1][j+1] to output[2i+1][j+2j+1].
"""

import numpy as np

def transform(input_grid):
    # Initialize a 4x4 output grid filled with zeros.
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the 2x2 input grid.
    for i in range(2):
        for j in range(2):
            # Replicate each input cell to its corresponding 2x2 block in the output grid.
            output_grid[i*2][j*2] = input_grid[i][j]
            output_grid[i*2+1][j*2] = input_grid[i][j]
            output_grid[i*2][j*2+1] = input_grid[i][j]
            output_grid[i*2+1][j*2+1] = input_grid[i][j]

    return output_grid
```
