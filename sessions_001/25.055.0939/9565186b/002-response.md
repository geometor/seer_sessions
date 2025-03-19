# 9565186b • 002 • example_1 • investigate_coder

---
```python
"""
Identify all pixels in the input grid.
If a pixel's color is blue (1) or azure (8), replace it with gray (5).
If a pixel's color is red (2), it remains unchanged.
Output the modified grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # iterate through each cell of the grid
    for i in range(rows):
        for j in range(cols):
            # change output pixels based on the transformation rule
            if input_grid[i][j] == 1 or input_grid[i][j] == 8:
                output_grid[i][j] = 5
            elif input_grid[i][j] == 2:
                output_grid[i][j] = 2 #Red remains red

    return output_grid
```
