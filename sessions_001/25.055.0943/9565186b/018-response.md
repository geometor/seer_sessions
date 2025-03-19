# 9565186b • 018 • refine_coder

---
```python
"""
Replace all pixels colored azure with pixels colored gray.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = [row[:] for row in input_grid]

    # iterate through the grid and replace azure with gray
    for i in range(len(output_grid)):
        for j in range(len(output_grid[i])):
            if output_grid[i][j] == 8:
                output_grid[i][j] = 5

    return output_grid
```
