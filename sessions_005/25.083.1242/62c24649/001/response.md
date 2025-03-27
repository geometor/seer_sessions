```python
"""
The input grid is transformed into a larger output grid by scaling up each pixel to a 2x2 block.
The scaling is done by simple duplication, then each 2x2 block is replicated.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into the output grid by scaling each pixel to a 2x2 block and mirroring.
    """
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = [[0] * output_width for _ in range(output_height)]

    # Iterate through each cell of the input grid
    for i in range(input_height):
        for j in range(input_width):
            # Copy the pixel's value to a 2x2 block in the output grid
            output_grid[2*i][2*j] = input_grid[i][j]
            output_grid[2*i+1][2*j] = input_grid[i][j]
            output_grid[2*i][2*j+1] = input_grid[i][j]
            output_grid[2*i+1][2*j+1] = input_grid[i][j]

    return output_grid
```
