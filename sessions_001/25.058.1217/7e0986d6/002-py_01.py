"""
Iterates through each pixel in the input grid. Preserves pixels of colors that are orthogonally adjacent to at least one 0 (white pixel). Colors not adjacent to 0 are changed to 0 in the output grid.
"""

import numpy as np

def is_adjacent_to_zero(grid, row, col):
    # Check if a cell is within bounds and adjacent to a zero
    rows, cols = grid.shape
    # Check up
    if row > 0 and grid[row-1, col] == 0:
        return True
    # Check down
    if row < rows - 1 and grid[row+1, col] == 0:
        return True
    # Check left
    if col > 0 and grid[row, col-1] == 0:
        return True
    # Check right
    if col < cols - 1 and grid[row, col+1] == 0:
        return True
    return False

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel's color is not 0
            if input_grid[row, col] != 0:
                # Check if the pixel is adjacent to a 0 pixel
                if not is_adjacent_to_zero(input_grid, row, col):
                    # If not adjacent to 0, change to 0
                    output_grid[row, col] = 0

    return output_grid