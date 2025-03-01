"""
The input grid is transformed into an output grid that is double the height and width of the input. Every azure (8) pixel in the input grid becomes a 2x2 block of azure pixels in the output grid, starting at the position of original pixel multiplied by two. Pixels of other colors in the input grid do not appear at all in the output grid.
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