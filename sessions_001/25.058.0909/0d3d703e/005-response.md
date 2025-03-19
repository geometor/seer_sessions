# 4-0d3d703e • 005 • refine_coder

---
```python
"""
The transformation rule involves a direct color substitution within the
grid. The colors green (3), blue (1), and red (2) are consistently replaced
with yellow (4), gray (5), and magenta (6) respectively.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the output grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Apply the value mapping.
            if output_grid[i, j] == 3:
                output_grid[i, j] = 4
            elif output_grid[i, j] == 1:
                output_grid[i, j] = 5
            elif output_grid[i, j] == 2:
                output_grid[i, j] = 6

    return output_grid
```
