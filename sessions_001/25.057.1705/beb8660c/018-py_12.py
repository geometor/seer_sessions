"""
The output grid is the same size as the input grid.
All pixels that are not part of a 2x2 black square in the input grid are set to white (0) in the output grid.
Pixels that are part of a 2x2 black square in the input grid remain black (0) in the output grid.
"""

import numpy as np

def find_2x2_black_squares(grid):
    """
    Finds the coordinates of all 2x2 black squares in the grid.
    Returns a list of tuples, where each tuple represents the top-left corner
    of a 2x2 square.
    """
    squares = []
    rows, cols = len(grid), len(grid[0])
    for row in range(rows - 1):
        for col in range(cols - 1):
            if (grid[row][col] == 0 and
                grid[row+1][col] == 0 and
                grid[row][col+1] == 0 and
                grid[row+1][col+1] == 0):
                squares.append((row, col))
    return squares

def transform(input_grid):
    """
    Transforms the input grid by keeping only 2x2 black squares.
    """
    # Initialize the output grid as all white.
    output_grid = np.full_like(input_grid, 0)

    # Find all 2x2 black squares in the input grid.
    squares = find_2x2_black_squares(input_grid)

    # Keep the pixels of the 2x2 squares black in the output grid.
    for row, col in squares:
        output_grid[row][col] = 0
        output_grid[row+1][col] = 0
        output_grid[row][col+1] = 0
        output_grid[row+1][col+1] = 0

    return output_grid.tolist()