"""
Iterate through each pixel in the input grid. If the pixel is yellow (color 4), keep it unchanged. If the pixel is not yellow, check if it is adjacent to any yellow pixel (horizontally or vertically). If the non-yellow pixel IS adjacent to a yellow pixel, change it to gray (color 5). If the non-yellow pixel is NOT adjacent to a yellow pixel, keep original color. Return the modified grid.
"""

import numpy as np

def is_adjacent_to_yellow(grid, row, col):
    """
    Checks if a pixel at grid[row][col] is adjacent to a yellow pixel.

    Args:
        grid: The 2D numpy array representing the grid.
        row: The row index of the pixel.
        col: The column index of the pixel.

    Returns:
        True if the pixel is adjacent to a yellow pixel, False otherwise.
    """
    rows, cols = grid.shape
    # Check adjacent cells (up, down, left, right)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row, new_col] == 4:
            return True  # Found a yellow neighbor
    return False

def transform(input_grid):
    """
    Transforms the input grid based on the adjacency to yellow pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate over each cell
    for i in range(rows):
        for j in range(cols):
            # Keep yellow pixels unchanged
            if output_grid[i, j] == 4:
                continue
            # Check for adjacency to yellow and change to gray if needed,
            # otherwise, keep the original value
            elif is_adjacent_to_yellow(output_grid, i, j):
                output_grid[i, j] = 5

    return output_grid