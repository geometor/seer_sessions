```python
"""
The transformation identifies enclosed '0's between '2's, either horizontally or vertically, and replaces the '0' with a '4'. The source '2' pixels do not change, they trigger the fill.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # change output pixels 
    # horizontal scan and fill
    for i in range(rows):
        for j in range(cols - 2):
            if input_grid[i, j] == 2 and input_grid[i, j+1] == 0 and input_grid[i, j+2] == 2:
                output_grid[i, j+1] = 4

    # vertical scan and fill
    for i in range(rows - 2):
        for j in range(cols):
            if input_grid[i, j] == 2 and input_grid[i+1, j] == 0 and input_grid[i+2, j] == 2:
                output_grid[i+1, j] = 4

    return output_grid
```