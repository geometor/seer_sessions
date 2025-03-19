"""
The task involves extracting the largest square subgrid composed entirely of gray (5) pixels from the input grid.
"""

import numpy as np

def find_all_squares(grid, color):
    """
    Finds all square subgrids of a specified color in a grid.
    Returns a list of tuples: (row_start, col_start, size).
    """
    squares = []
    rows, cols = grid.shape
    max_size = min(rows, cols)
    for size in range(1, max_size + 1):
        for row_start in range(0, rows - size + 1):
            for col_start in range(0, cols - size + 1):
                subgrid = grid[row_start:row_start+size, col_start:col_start+size]
                if np.all(subgrid == color):
                    squares.append((row_start, col_start, size))
    return squares

def transform(input_grid):
    """
    Extracts the largest square subgrid of gray (5) pixels.
    """
    input_grid = np.array(input_grid)

    # Find all squares of color 5 (gray).
    gray_squares = find_all_squares(input_grid, 5)

    # If no gray squares are found, return an empty grid (or a 1x1 grid with 0, per ARC rules).
    if not gray_squares:
        return [[0]] # Or [] depending if empty grids are allowed.  [[0]] is safer.

    # Find the largest square.
    largest_square = max(gray_squares, key=lambda x: x[2])

    # Extract the largest square.
    row_start, col_start, size = largest_square
    output_grid = input_grid[row_start:row_start+size, col_start:col_start+size]
    
    return output_grid.tolist()