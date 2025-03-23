```python
"""
Increase each digit by one, except:
- change 5 -> 1,
- change 6 -> 2, and
- change 9 -> 8.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # change output pixels 
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 5:
                output_grid[i, j] = 1
            elif output_grid[i, j] == 6:
                output_grid[i, j] = 2
            elif output_grid[i, j] == 9:
                output_grid[i, j] = 8
            elif output_grid[i,j] in [1,2,3,4,8]:
                output_grid[i,j] += 1

    return output_grid
```