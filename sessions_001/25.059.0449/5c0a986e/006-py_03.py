"""
The transformation rule identifies 2x2 squares in the input grid and places pixels of the same color adjacent to the square in the output, forming a '+' shape centered on the original square's location.
"""

import numpy as np

def find_squares(grid, size=2):
    """Finds all squares of the specified size in the grid."""
    squares = []
    for r in range(grid.shape[0] - size + 1):
        for c in range(grid.shape[1] - size + 1):
            if np.all(grid[r:r+size, c:c+size] == grid[r, c]) and grid[r,c] != 0:
                squares.append((grid[r, c], (r, c)))
    return squares

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid) # Initialize with zeros
    squares = find_squares(input_grid)

    for color, (r, c) in squares:
        # Place pixels above, below, left, and right of the 2x2 square.

        # Above
        if r - 1 >= 0:
            output_grid[r - 1, c] = color
            output_grid[r - 1, c+1] = color

        # Below
        if r + 2 < output_grid.shape[0]:
            output_grid[r + 2, c] = color
            output_grid[r + 2, c + 1] = color

        # Left
        if c - 1 >= 0:
            output_grid[r, c - 1] = color
            output_grid[r+1, c - 1] = color

        # Right
        if c + 2 < output_grid.shape[1]:
            output_grid[r, c + 2] = color
            output_grid[r + 1, c + 2] = color

    return output_grid