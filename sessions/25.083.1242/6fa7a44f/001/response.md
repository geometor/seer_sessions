```python
"""
The input grid is reflected across a horizontal axis and the order of rows in reflection is reversed. The output grid's height is double the input grid's height. The input is copied to the top half of the output. The bottom half is the reflected and reordered input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_grid = np.zeros((input_height * 2, input_width), dtype=int)

    # Copy the input to the top half of output
    for i in range(input_height):
        output_grid[i] = input_grid[i]

    # Reflect and Reorder: Copy each row from input and place into the output grid in reverse order, below the original.
    for i in range(input_height):
        output_grid[input_height * 2 - 1 - i] = input_grid[i]

    return output_grid
```