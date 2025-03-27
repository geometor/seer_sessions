```python
"""
The input grid is duplicated horizontally to create an output grid that is twice the width of the input. The left half of the output is identical to the input, and the right half is also identical to the input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_width = 2 * input_width
    output_grid = np.zeros((input_height, output_width), dtype=int)

    # change output pixels 
    # Populate the left half of the output grid with the input grid
    for i in range(input_height):
        for j in range(input_width):
            output_grid[i, j] = input_grid[i][j]

    # Populate the right half of the output grid with the input grid
    for i in range(input_height):
        for j in range(input_width):
            output_grid[i, j + input_width] = input_grid[i][j]

    return output_grid
```