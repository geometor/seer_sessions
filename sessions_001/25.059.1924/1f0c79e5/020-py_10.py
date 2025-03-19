"""
Scan the input grid for any 2x2 squares. Record the row and column indices of the top-left corner of each found square. Create an output grid of the same size as the input. Draw the main diagonal line (y = -x) on the output grid using magenta color. The key idea is that any 2x2 squares must have top-left corners that lie on the output diagonal.
"""

import numpy as np

def find_2x2_squares(grid):
    """Finds all 2x2 squares in a grid and returns the top-left corner coordinates."""
    squares = []
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] == grid[i + 1, j] == grid[i, j + 1] == grid[i + 1, j + 1]):
                squares.append((i, j))
    return squares

def transform(input_grid):
    # Initialize output_grid as a zero-filled array of the same size as the input.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find 2x2 squares and store their top-left corner coordinates.
    squares = find_2x2_squares(input_grid)

    # Iterate through all possible positions in the output grid
    for i in range(rows):
        for j in range(cols):
            # Check if the current position is on the main diagonal (y = -x <=> i + j = rows - 1)
            if i + j == rows - 1:
                output_grid[i, j] = 6  # Set the diagonal pixels to magenta (6)

    return output_grid