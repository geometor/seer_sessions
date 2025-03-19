# 2204b7a8 • 012 • refine_coder

---
```python
"""
1.  Iterate through each pixel in the input grid.
2.  If a pixel's color is green (3), change its color to yellow (4).
3.  If a pixel's color is yellow (4) and it is located on the 6th row from the top (index 5), change all the yellow (4) pixels on that row to orange (7).
4.  Otherwise, keep the pixel's original color.
5.  Output the modified grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)  # Initialize output grid as a copy of the input
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    for i in range(rows):
        for j in range(cols):
            # Change green (3) to yellow (4)
            if output_grid[i, j] == 3:
                output_grid[i, j] = 4

    for i in range(rows):
        for j in range(cols):
            #change all yellow(4) to orange (7) on 6th row, index 5
            if i == 5 and output_grid[i,j] == 4:
                for k in range(cols):
                    if output_grid[i,k] == 4:
                         output_grid[i,k] = 7

    return output_grid
```
