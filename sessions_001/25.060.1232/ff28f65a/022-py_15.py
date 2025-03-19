"""
The program finds 2x2 red squares in the input, and for each, creates a blue pixel on the first row output grid with an x position corresponding to original position / 2.
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
    output_grid = np.zeros((3, 3), dtype=int)

    # Find 2x2 red squares
    squares = find_squares(input_grid, 2, 2)

    # Represent each square as a blue pixel in the output
    for square in squares:
        row, col = square
        output_row = 0
        output_col = col // 2
        output_grid[output_row, output_col] = 1
        

    return output_grid