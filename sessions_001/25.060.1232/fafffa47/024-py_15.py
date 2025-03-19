"""
The input grid is compressed vertically by a factor of two. Every two consecutive rows in the input grid are combined to produce a single row in the output grid. For each column, examine the two pixels from the two consecutive input rows. If either of the input pixels is Maroon (9), the corresponding output pixel is Red (2). Otherwise, the output is white (0).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height // 2
    output_width = input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels 
    for i in range(output_height):
        for j in range(output_width):
            # Consider two rows at a time from the input_grid
            val1 = input_grid[2*i, j]
            val2 = input_grid[2*i + 1, j]

            # color mapping
            if val1 == 9 or val2 == 9:
                output_grid[i,j] = 2 # maroon becomes red
            else:
                output_grid[i,j] = 0 # otherwise white

    return output_grid