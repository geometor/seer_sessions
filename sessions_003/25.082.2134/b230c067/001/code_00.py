"""
The transformation identifies contiguous regions of azure (8) pixels in the input grid. 
It then replaces the "border" azure pixels of each region with red (2) pixels and the remaining interior azure pixels with blue (1) pixels. 
Background (0) pixels remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
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

def is_border(grid, row, col, color):
    """Checks if a cell of the specified color is a border cell."""
    if grid[row, col] != color:
        return False
    for r, c in get_neighbors(grid, row, col):
        if grid[r, c] != color:
            return True
    return False

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid to find azure regions and apply replacements
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 8:  # Found an azure pixel
                if is_border(input_grid, row, col, 8):
                    output_grid[row, col] = 2  # Replace border azure with red
                else:
                    output_grid[row, col] = 1  # Replace interior azure with blue

    return output_grid