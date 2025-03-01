# d13f3404 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves expanding a 3x3 input grid into a 6x6 output grid. 
The non-zero elements of the input grid are copied diagonally in the output grid.
The input grid is traversed diagonally (top-left to bottom-right)
The output grid's diagonal starting from corresponding scaled input coordinates (2*i, 2*j) gets the values.
Zeros in the input are treated as background, and remaining cells in the output are filled with zeros.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as 6x6 with all zeros
    output_grid = np.zeros((6, 6), dtype=int)

    # Traverse the input grid diagonally (top-left to bottom-right).
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Copy input values to output grid. Start at 2*i, 2*j
            if input_grid[i,j] != 0:
                for k in range(6 - (2*i)):
                    if (2*j)+k < 6:
                        output_grid[(2*i) + k, (2*j) + k] = input_grid[i, j]


    return output_grid
```
