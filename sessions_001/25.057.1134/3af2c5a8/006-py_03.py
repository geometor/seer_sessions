"""
1.  **Initialization:** Create an output grid that is twice the height and twice the width of the input grid. Initialize all its cells to black (0).

2.  **Azure Pixel Expansion:** For each pixel in the input grid:
    *   If the pixel is azure (8), then in the output grid, create a 2x2 block of azure pixels.
    *   The top-left corner of this 2x2 block will be at coordinates (row \* 2, column \* 2), where 'row' and 'column' are the coordinates of the original azure pixel in the input grid.
    *   do nothing with non-azure pixels, leave the background black.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels 
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 8:
                # expand azure pixel to 2x2 block
                output_grid[row * 2, col * 2] = 8
                output_grid[row * 2 + 1, col * 2] = 8
                output_grid[row * 2, col * 2 + 1] = 8
                output_grid[row * 2 + 1, col * 2 + 1] = 8

    return output_grid