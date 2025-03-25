"""
The transformation rule involves identifying non-white pixels in the input grid. If a non-white pixel is not on an edge,
it's replaced by a 3x3 block of blue (1) pixels centered on the original pixel's location, but the center pixel retains its original color.
If the pixel IS on an edge and a 3x3 block cannot be placed, the original value is copied unchanged.
"""

import numpy as np

def can_place_3x3(grid, row, col):
    """
    Checks if a 3x3 block can be placed centered at (row, col) without going out of bounds.
    """
    rows, cols = grid.shape
    return row > 0 and row < rows - 1 and col > 0 and col < cols - 1

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for row in range(rows):
        for col in range(cols):
            # Identify "target pixels" (non-white pixels)
            if input_grid[row, col] != 0:
                # Check if a 3x3 block can be placed
                if can_place_3x3(input_grid, row, col):
                    # Replace with a 3x3 block of blue (1)
                    for r in range(row - 1, row + 2):
                        for c in range(col - 1, col + 2):
                            output_grid[r, c] = 1
                    # restore original color at center
                    output_grid[row,col] = input_grid[row,col]
                else:
                    # copy value from input
                    output_grid[row,col] = input_grid[row,col]


    return output_grid