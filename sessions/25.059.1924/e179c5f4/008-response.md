# e179c5f4 • 008 • refine_coder

---
```python
"""
1.  Identify Input Pixels: Examine each pixel in the input grid.
2.  Preserve Non-Zero/One Values: If a pixel's value is *not* 0 or 1, its value in the output grid remains the *same* as in the input grid.
3.  Transform 0 and 1 Values: If a pixel's value *is* 0 or 1:
    *   Calculate the sum of its row and column indices (`row + col`).
    *   If the sum is even:
        *   If the input value is 0, the output value is 8.
        *   If the input value is 1, the output value is 1.
    *   If the sum is odd:
        *   If the input value is 0, the output value is 1.
        *   If the input value is 1, the output value is 8.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # change output pixels 
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0 or input_grid[i,j] == 1:
                if (i + j) % 2 == 0:
                    if input_grid[i, j] == 0:
                        output_grid[i, j] = 8
                    else: # input is 1
                        output_grid[i,j] = 1
                else: # (i + j) is odd
                    if input_grid[i, j] == 0:
                        output_grid[i,j] = 1
                    else: # input is 1
                        output_grid[i,j] = 8
            # else: pixel value remains the same (implicit in np.copy)

    return output_grid
```

