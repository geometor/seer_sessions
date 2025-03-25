```python
"""
The input grid is transformed into an output grid with the same height but twice the width. Each column of the input grid is duplicated in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_width = input_width * 2
    output_height = input_height
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    for i in range(input_height):
        for j in range(input_width):
            output_grid[i, 2*j] = input_grid[i][j]
            output_grid[i, 2*j + 1] = input_grid[i][j]

    return output_grid
```