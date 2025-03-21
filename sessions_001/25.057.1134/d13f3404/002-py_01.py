"""
The input grid is transformed into an output grid with double the dimensions. 
Each non-white pixel in the input grid generates a diagonal line of the same color in the output grid. 
The diagonal starts at the doubled coordinates of the input pixel and extends to the bottom-right of the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with double the dimensions, filled with white (0)
    input_rows, input_cols = len(input_grid), len(input_grid[0])
    output_rows, output_cols = 2 * input_rows, 2 * input_cols
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # iterate through each pixel of the input grid
    for i in range(input_rows):
        for j in range(input_cols):
            pixel_color = input_grid[i][j]
            # if the pixel is not white
            if pixel_color != 0:
                # calculate the starting position in the output grid (doubled coordinates)
                start_row, start_col = 2 * i, 2 * j
                # draw a diagonal line of the same color
                row, col = start_row, start_col
                while row < output_rows and col < output_cols:
                    output_grid[row][col] = pixel_color
                    row += 1
                    col += 1

    return output_grid