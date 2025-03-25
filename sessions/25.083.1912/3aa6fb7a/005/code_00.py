"""
The transformation identifies azure (color 8) pixels in the input grid.  It then adds blue (color 1) pixels immediately adjacent to the azure pixels.  A blue pixel is added if and only if:

1.  The cell is currently empty (color 0).
2.  The cell is directly adjacent (horizontally or vertically, *not* diagonally) to at least one azure pixel. The position of the azure pixel determines the position of the added blue.

The blue pixels essentially "extend" existing azure structures by one pixel, but they do not connect non-adjacent segments of azure.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Returns the coordinates of the neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is azure
            if input_grid[r, c] == 8:
                # Get the neighbors of the current azure pixel
                neighbors = get_neighbors(input_grid, r, c)
                # Check each neighbor
                for nr, nc in neighbors:
                    # If the neighbor is empty (0), change it to blue (1) in the output grid
                    if input_grid[nr, nc] == 0:
                        output_grid[nr, nc] = 1

    return output_grid