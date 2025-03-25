```python
"""
The transformation rule is to replicate the input pixel as a 2x2 square with the same color and superimpose a cross, or an X, of blue (1) pixels across the entire output grid, and to double the size of the original grid to create a new output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # find the non-zero pixel in input and expand
    for r in range(input_height):
        for c in range(input_width):
            if input_grid[r, c] != 0:
                color = input_grid[r, c]
                output_grid[2*r:2*r+2, 2*c:2*c+2] = color
                break  # only one non zero pixel
        else:
            continue
        break

    # Create Diagonal Cross
    for i in range(output_height):
        output_grid[i, i] = 1  # Top-left to bottom-right
        output_grid[i, output_width - 1 - i] = 1  # Top-right to bottom-left

    return output_grid
```