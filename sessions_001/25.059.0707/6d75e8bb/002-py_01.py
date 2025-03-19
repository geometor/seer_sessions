"""
The transformation identifies contiguous regions of azure (8) pixels in the input grid.  It then changes the color of the "interior" azure pixels to red (2), while preserving the azure pixels on the perimeter of these regions. White (0) pixels remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns the valid neighbors of a cell in a grid, no diagonals.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def is_interior(grid, row, col, color):
    """
    Checks if a pixel at (row, col) of the given color is an interior pixel.
    An interior pixel is surrounded on all four sides (up, down, left, right) by pixels of the same color.
    """
    if grid[row, col] != color:
        return False

    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        if grid[r, c] != color:
            return False  # Not interior if any neighbor is a different color
    return True


def transform(input_grid):
    """
    Transforms the input grid according to the rule:  Fills interior azure regions with red.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the grid
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is azure and an interior pixel
            if is_interior(input_grid, row, col, 8):
                output_grid[row, col] = 2  # Change to red
            # else, input grid is copied, no need to change.

    return output_grid