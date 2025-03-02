"""
1.  **Input:** A 2D grid of pixels (input_grid), where each pixel has a color value.
2.  **Output:** A 2D grid of pixels (output_grid) that is a scaled-up version of the input grid.
3.  **Scaling:** The output_grid's height is three times the input_grid's height. The output_grid's width is three times the input_grid's width.
4.  **Transformation:** For each pixel in the input_grid:
    *   Expand the pixel into a 3x3 block of pixels in the output_grid.
    *   The color of all pixels in the 3x3 block is the same as the original input pixel's color.
    *   The position (top left) of each block on the new grid (i,j) is calculated from the position of each pixel on the old grid (x,y) such that i = 3x, j = 3y.
5. The process occurs for all pixels in the grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with dimensions scaled by 3x.
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]
    output_grid = np.zeros((input_height * 3, input_width * 3), dtype=int)

    # Iterate through each pixel of the input grid.
    for i in range(input_height):
        for j in range(input_width):
            # Get the color of the current pixel.
            color = input_grid[i, j]

            # Create the 3x3 block in the output grid.
            for row_offset in range(3):
                for col_offset in range(3):
                    output_grid[i * 3 + row_offset, j * 3 + col_offset] = color

    return output_grid