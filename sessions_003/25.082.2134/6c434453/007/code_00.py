"""
The transformation identifies groups of three adjacent blue (1) pixels forming either a horizontal, vertical, or diagonal line. The central blue pixel in each such group is changed to red (2). Blue pixels that are adjacent to any red pixel that remains part of a line of three red pixels *after* the first transformation are changed to white (0). Isolated blue pixels and blue lines of lengths other than 3 are not changed.
"""

import numpy as np

def is_center_of_blue_line(grid, row, col):
    """Checks if the pixel at (row, col) is the center of a 3-blue-pixel line."""
    rows, cols = grid.shape
    color = 1  # Blue

    # Check horizontal
    if col > 0 and col < cols - 1:
        if grid[row, col - 1] == color and grid[row, col + 1] == color:
            return True

    # Check vertical
    if row > 0 and row < rows - 1:
        if grid[row - 1, col] == color and grid[row + 1, col] == color:
            return True

    # Check top-left to bottom-right diagonal
    if row > 0 and col > 0 and row < rows - 1 and col < cols - 1:
        if grid[row - 1, col - 1] == color and grid[row + 1, col + 1] == color:
            return True

    # Check top-right to bottom-left diagonal
    if row > 0 and col < cols - 1 and row < rows - 1 and col > 0:
        if grid[row - 1, col + 1] == color and grid[row + 1, col - 1] == color:
            return True

    return False

def is_part_of_red_line(grid, row, col):
    """Checks if the pixel at (row, col) is part of a 3-red-pixel line."""
    rows, cols = grid.shape
    color = 2  # Red

    # Check horizontal
    if col > 0 and col < cols - 1:
        if grid[row, col - 1] == color and grid[row, col + 1] == color:
            return True

    # Check vertical
    if row > 0 and row < rows - 1:
        if grid[row - 1, col] == color and grid[row + 1, col] == color:
            return True

    # Check top-left to bottom-right diagonal
    if row > 0 and col > 0 and row < rows - 1 and col < cols - 1:
        if grid[row - 1, col - 1] == color and grid[row + 1, col + 1] == color:
            return True

    # Check top-right to bottom-left diagonal
    if row > 0 and col < cols - 1 and row < rows - 1 and col > 0:
        if grid[row - 1, col + 1] == color and grid[row + 1, col - 1] == color:
            return True

    return False

def is_adjacent(row1, col1, row2, col2):
    """Checks if two cells are adjacent (including diagonals)."""
    return abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # First, change the center of 3-blue-pixel lines to red
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 1:  # Blue pixel
                if is_center_of_blue_line(input_grid, row, col):
                    output_grid[row, col] = 2  # Change to red

    # Create a copy to iterate over while modifying output
    intermediate_grid = np.copy(output_grid)

    # Now, iterate through the grid again, applying the adjacency rule
    for row in range(rows):
        for col in range(cols):
            if intermediate_grid[row, col] == 1: #if it is blue
                for r in range(rows):
                    for c in range(cols):
                      if intermediate_grid[r,c] == 2: #red
                        if is_part_of_red_line(intermediate_grid,r,c):
                            if is_adjacent(row, col, r, c):
                                output_grid[row,col] = 0 #make blue pixel white
    return output_grid