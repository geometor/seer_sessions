# 75b8110e • 006 • refine_coder

---
```python
"""
Divide the input grid into non-overlapping 2x2 blocks. For each block, inspect the pixel values.
If the block contains a green (3) pixel, output green (3). Otherwise, output blue (1). Construct a
new grid from these selected pixels.
"""

import numpy as np

def get_pixel_value(block, value):
    """
    Helper function to return the first index i, j of a value, or -1,-1 if not
    present.
    """
    for i in range(block.shape[0]):
        for j in range(block.shape[1]):
            if block[i,j] == value:
                return i, j
    return -1,-1

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_height = input_height // 2
    output_width = input_width // 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    for i in range(output_height):
        for j in range(output_width):
            # Define the 2x2 block in the input grid
            block = input_grid[i*2:(i+1)*2, j*2:(j+1)*2]

            # Check for green (3) in the block
            green_row, green_col = get_pixel_value(block, 3)
            if green_row != -1:
                output_grid[i,j] = 3 # Output green
            else:
                output_grid[i,j] = 1   #else output blue

    return output_grid.tolist()
```

