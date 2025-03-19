"""
1.  **Expansion:** Each non-white pixel in the input grid is expanded into a 2x2 block of the same color in the output grid. The top-left of each 2x2 block will map to row index `r*2`, col index `c*2`, where `r` and `c` are the input row and column of a non-white pixel.
2. **Background:** Create an output grid and fill every cell with the value `2`.
3. **Replacement:** Go through each pixel of the input. Replace the area in output corresponding to non-zero pixels, determined by the rule in step 1.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_height = input_height * 2
    output_width = input_width * 2

    # initialize output_grid with all 2s
    output_grid = np.full((output_height, output_width), 2)

    # Iterate through input grid
    for row_index in range(input_height):
        for col_index in range(input_width):
            input_pixel_value = input_grid[row_index][col_index]
            #if a non-white cell
            if input_pixel_value != 0:
              # set the corresponding 2x2 block in output.
              output_grid[row_index*2:row_index*2+2, col_index*2:col_index*2+2] = input_pixel_value

    return output_grid