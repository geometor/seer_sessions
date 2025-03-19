"""
Each pixel in the input grid is expanded into a 2x2 block of the same color in the output grid. The entire expanded matrix is surrounded by white borders.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with dimensions (2 * input_height + 2) x (2 * input_width + 2) and fill with 0 (white)
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((2 * input_height + 2, 2 * input_width + 2), dtype=int)

    # iterate through each pixel of the input grid
    for row in range(input_height):
        for col in range(input_width):
            # get the color of the current input pixel
            color = input_grid[row, col]
            
            # calculate the starting position for the 2x2 block in the output grid
            output_row = 2 * row + 1
            output_col = 2 * col + 1
            
            # fill the 2x2 block with the same color
            output_grid[output_row:output_row+2, output_col:output_col+2] = color

    return output_grid