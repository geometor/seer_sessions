"""
The program identifies 2x2 red squares in the input grid and represents them as blue pixels in the output grid. The output grid has one row, and its width is three less than the input grid's width. For each 2x2 red square, a blue pixel is placed in the output grid at row 0, and at a column one greater than the column of the top-left pixel of the red square.
"""

import numpy as np

def find_squares(grid, size, color):
    squares = []
    for row in range(grid.shape[0] - size + 1):
        for col in range(grid.shape[1] - size + 1):
            subgrid = grid[row:row+size, col:col+size]
            if np.all(subgrid == color):
                squares.append((row, col))
    return squares

def transform(input_grid):
    # initialize output_grid
    output_width = input_grid.shape[1] - 3
    output_grid = np.zeros((1, output_width), dtype=int)

    # Find 2x2 red squares
    squares = find_squares(input_grid, 2, 2)

    # Represent each square as a blue pixel in the output
    for square in squares:
        row, col = square
        output_row = 0
        output_col = col + 1
        if output_col < output_width:
          output_grid[output_row, output_col] = 1
        

    return output_grid