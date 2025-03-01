"""
Double the dimensions of the input grid. Copy yellow pixels to the output grid at specific positions, and replicate these in a mirrored fashion. 
Create an azure checkerboard pattern, and frame certain areas with azure.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with doubled dimensions
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate Yellow
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 4:
                output_grid[row * 2 + 1, col * 2 + 1] = 4
                output_grid[row * 2 + 1, (input_width*2-2) - col * 2] = 4

    # Fill with Azure background
    for row in range(output_height):
        for col in range(output_width):
            if (row + col) % 2 == 0:
                output_grid[row, col] = 8

    # Overlay Border, not needed with this sample
    #for row in range(output_height):
    #    for col in range(output_width):
    #        if output_grid[row,col] == 0:
    #            if row > 0 and output_grid[row-1,col] == 8:
    #                 output_grid[row,col] = 8
    #            elif row < output_height -1 and output_grid[row+1, col] == 8:
    #                 output_grid[row,col] = 8
    #            elif col > 0 and output_grid[row,col-1] == 8:
    #                 output_grid[row,col] = 8
    #            elif col < output_width - 1 and output_grid[row, col+1] == 8:
    #                 output_grid[row,col] = 8

    return output_grid