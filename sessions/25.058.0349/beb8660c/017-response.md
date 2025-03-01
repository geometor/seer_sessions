# beb8660c • 017 • refine_coder

---
```python
"""
The transformation involves swapping the values of the first two rows of the input grid. Specifically, the elements at indices [0][0] and [0][1] of the first two rows are swapped with the elements at [1][0] and [1][1].
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    #Ensure that there are at least two rows to swap, otherwise return input
    if output_grid.shape[0] < 2:
      return output_grid

    # Swap elements between the first two rows
    if output_grid.shape[1] >=2: #ensure there are two columns
        temp00 = output_grid[0, 0]
        temp10 = output_grid[1, 0]
        output_grid[0, 0] = temp10
        output_grid[1, 0] = temp00
        temp01 = output_grid[0,1]
        temp11 = output_grid[1,1]
        output_grid[0,1] = temp11
        output_grid[1,1] = temp01
    elif output_grid.shape[1] == 1: #if only one column, then swap only one element
        temp00 = output_grid[0, 0]
        temp10 = output_grid[1, 0]
        output_grid[0, 0] = temp10
        output_grid[1, 0] = temp00

    return output_grid
```
