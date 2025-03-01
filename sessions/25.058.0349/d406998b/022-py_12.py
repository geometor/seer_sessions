"""
Iterate through the input grid. Identify all gray (5) pixels. Determine groups
of adjacent gray pixels that form a continuous line (horizontal or vertical).
Convert all gray pixels in such lines to green (3). All other pixels remain
unchanged.
"""

import numpy as np

def find_connected_gray_pixels(grid, start_row, start_col, visited):
    """
    Finds all gray pixels connected to a starting gray pixel, either
    horizontally or vertically, using Depth-First Search (DFS).

    Args:
        grid: The input grid.
        start_row: Starting row index.
        start_col: Starting column index.
        visited: A set of visited pixel coordinates.

    Returns:
        A set of (row, col) tuples representing connected gray pixels.
    """
    rows, cols = grid.shape
    connected_pixels = set()
    stack = [(start_row, start_col)]

    while stack:
        row, col = stack.pop()
        if (row, col) in visited or grid[row, col] != 5:
            continue

        visited.add((row, col))
        connected_pixels.add((row, col))

        # Check adjacent cells (up, down, left, right)
        if row > 0:
            stack.append((row - 1, col))  # Up
        if row < rows - 1:
            stack.append((row + 1, col))  # Down
        if col > 0:
            stack.append((row, col - 1))  # Left
        if col < cols - 1:
            stack.append((row, col + 1))  # Right

    return connected_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    visited = set()

    # Iterate and change output pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 5 and (r, c) not in visited:
                connected_set = find_connected_gray_pixels(output_grid, r, c, visited)
                # if a connected set of gray pixels exists
                if connected_set:
                  for gray_row, gray_col in connected_set:
                    output_grid[gray_row,gray_col] = 3 #change all to green

    return output_grid