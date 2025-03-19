# 94f9d214 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation takes the top 3x3 input area, replaces the 3 by 2 and keeps the 0. The 4th column of the top 3 rows of the input becomes the 4th column of the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as 4x4 with all zeros
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the top-left 3x3 subgrid of the input
    for i in range(3):
        for j in range(3):
            # Map green (3) to red (2), and keep 0 as 0
            if input_grid[i][j] == 3:
                output_grid[i][j] = 2
            elif input_grid[i][j] == 0:
                output_grid[i][j] = 0

    # Process the 4th column of input to the 4th column of output, top 3 rows
    for i in range(3):
      if input_grid[i][3] == 3:
        output_grid[i][3] = 2

    return output_grid
```
