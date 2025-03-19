"""
1.  Identify all pixels that are azure (8). These are the termination points.
2.  Identify all pixels that are red (2). These are the starting points.
3.  For each red pixel:
    *   Create a path of yellow (4) pixels, extending in all four directions (up, down, left, right) from the red pixel.
    *   Terminate the path in a given direction when a cell is directly or diagonally adjacent to any azure (8) pixel.
    *   If a path segment in a direction connects to an existing yellow pixel, stop the path in that direction.
"""

import numpy as np

def find_all_pixels(grid, color):
    # Find the coordinates of all pixels with a specific color.
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def is_adjacent(grid, row, col, color):
    # Check if a cell is adjacent (including diagonally) to a cell of a specific color.
    rows, cols = grid.shape
    for r in range(max(0, row - 1), min(rows, row + 2)):
        for c in range(max(0, col - 1), min(cols, col + 2)):
            if (r != row or c != col) and grid[r, c] == color:
                return True
    return False

def is_connected_to_yellow(grid, row, col, output_grid):
    # Check if placing a yellow pixel at (row, col) would connect it to existing yellow pixels.
    rows, cols = output_grid.shape
    for r in range(max(0, row - 1), min(rows, row + 2)):
        for c in range(max(0, col - 1), min(cols, col + 2)):
            if (r != row or c != col) and output_grid[r, c] == 4:
                return True
    return False

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find all azure (8) pixels
    azure_pixels = find_all_pixels(input_grid, 8)

    # Find all red (2) pixels
    red_pixels = find_all_pixels(input_grid, 2)

    # Iterate over each red pixel
    for red_row, red_col in red_pixels:
        # Create paths of yellow (4) pixels in all four directions
        
        # Extend to the right
        for col in range(red_col + 1, input_grid.shape[1]):
            if is_adjacent(input_grid, red_row, col, 8):
                break
            if is_connected_to_yellow(input_grid, red_row, col, output_grid):
                break
            output_grid[red_row, col] = 4

        # Extend to the left
        for col in range(red_col - 1, -1, -1):
            if is_adjacent(input_grid, red_row, col, 8):
                break
            if is_connected_to_yellow(input_grid, red_row, col, output_grid):
                break
            output_grid[red_row, col] = 4
        
        # Extend upwards
        for row in range(red_row - 1, -1, -1):
            if is_adjacent(input_grid, row, red_col, 8):
                break
            if is_connected_to_yellow(input_grid, row, red_col, output_grid):
                break
            output_grid[row, red_col] = 4

        # Extend downwards
        for row in range(red_row + 1, input_grid.shape[0]):
            if is_adjacent(input_grid, row, red_col, 8):
                break
            if is_connected_to_yellow(input_grid, row, red_col, output_grid):
                break
            output_grid[row, red_col] = 4

    return output_grid