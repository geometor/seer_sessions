```python
"""
The input grid's non-zero pixels are expanded into a 9x9 grid. The mapping involves scaling the input coordinates to the output coordinates, ensuring the output grid is filled based on the relative position of non-zero pixels in the input.
"""

import numpy as np

def get_non_zero_color(input_grid):
    # Find the non-zero color in the input grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != 0:
                return input_grid[i, j]
    return 0

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # Find the non-zero color
    color = get_non_zero_color(input_grid)
    if color == 0:
      return output_grid

    # Find Input Pixels
    input_pixels = []
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r,c] == color:
                input_pixels.append((r,c))

    # change output pixels based on a mapping of input pixels

    for r_in, c_in in input_pixels:
        if (input_height > 1) and (input_width > 1):
            r_out = 8 - r_in * (8 // (input_height - 1))
            c_out = c_in * (8 // (input_width - 1))
        elif (input_height == 1) and (input_width > 1):
            r_out = 8 - r_in * 8
            c_out = c_in * (8 // (input_width - 1))
        elif (input_width == 1) and (input_height > 1):
            r_out = 8 - r_in * (8 // (input_height-1))
            c_out = c_in * 8
        else: # input_height == 1 and input_width == 1:
            r_out = 8 - r_in * 8
            c_out = c_in * 8

        output_grid[r_out, c_out] = color
        

    return output_grid
```