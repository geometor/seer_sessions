```python
"""
The input grid's digits are transformed to output digits according to the following mapping:

*   0 -> ? (we don't have an example yet, hold off assumption)
*   1 -> 5
*   2 -> 6
*   3 -> 4
*   4 -> 3
*   5 -> 1
*   6 -> 2
*   7 -> ? (we don't have an example yet, hold off assumption)
*   8 -> 9
*   9 -> 8

The transformation is applied to each cell of the input grid independently.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # change output pixels 
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 1:
                output_grid[i, j] = 5
            elif output_grid[i, j] == 2:
                output_grid[i, j] = 6
            elif output_grid[i, j] == 3:
                output_grid[i, j] = 4
            elif output_grid[i, j] == 4:
                output_grid[i, j] = 3
            elif output_grid[i, j] == 5:
                output_grid[i, j] = 1
            elif output_grid[i, j] == 6:
                output_grid[i, j] = 2
            elif output_grid[i, j] == 8:
                output_grid[i, j] = 9
            elif output_grid[i, j] == 9:
                output_grid[i, j] = 8

    return output_grid
```
