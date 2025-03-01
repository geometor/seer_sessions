"""
The transformation creates a 3x3 output grid.  If a 2x2 square of a single color exists in the input grid, the top-left cell of that 2x2 square in the input becomes the top-left cell of the output grid. All cells in the output grid are colored based on the color of the 2x2 square in the input grid.  If multiple 2x2 squares of different colors exist, only one is used for the output (prioritization rule not fully determined from limited data, but appears to favor earlier colors in color map). If no 2x2 square of a single color exists, the output is all white (0).
"""

import numpy as np

def find_2x2_squares(grid):
    """Finds all 2x2 squares of the same color in the grid."""
    squares = []
    for r in range(grid.shape[0] - 1):
        for c in range(grid.shape[1] - 1):
            subgrid = grid[r:r+2, c:c+2]
            if np.all(subgrid == subgrid[0, 0]):
                squares.append((r, c, subgrid[0, 0]))  # (row, col, color)
    return squares

def transform(input_grid):
    # Find all 2x2 squares of the same color.
    squares = find_2x2_squares(input_grid)

    # Initialize a 3x3 output grid filled with white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # If any 2x2 squares were found, use the first one to determine output color.
    if squares:
        # Prioritize squares (currently just takes the first).
        top_left_r, top_left_c, color = squares[0]

        # Fill the output grid with the color from the identified square.
        output_grid[:] = color
    
    return output_grid