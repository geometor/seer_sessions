# ce4f8723 • 002 • example_4 • investigate_coder

---
```python
"""
Extracts the top 4x4 section of the input grid, replaces blue (1) pixels with green (3), and keeps white (0) pixels unchanged to create a 4x4 output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as 4x4 with zeros.
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the top 4x4 section of the input grid
    for i in range(min(4, len(input_grid))):
        for j in range(min(4, len(input_grid[0]))):
            # Replace blue(1) with green(3), keep white(0)
            if input_grid[i][j] == 1:
                output_grid[i][j] = 3
            elif input_grid[i][j] == 0:
                output_grid[i][j] = 0

    return output_grid
```
