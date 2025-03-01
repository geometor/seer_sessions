"""
Find a connected set of azure pixels in the input grid, and change its value (color) to green.
If no azure pixels are present, return the original grid.
"""

import numpy as np

def find_connected_region(grid, start_row, start_col, color):
    # Find a connected region of a given color, starting from a given cell.
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    region = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        region.append((r, c))

        # Explore adjacent cells
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(start_row, start_col)
    return region

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the first azure pixel.
    start_row, start_col = None, None
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:
                start_row, start_col = r, c
                break  # Only find the first azure region
        if start_row is not None:
            break

    if start_row is None:  # No azure found
        return output_grid

    connected_region = find_connected_region(input_grid, start_row, start_col, 8)

    # Flood fill the connected region with green (3)
    for r, c in connected_region:
        output_grid[r, c] = 3

    return output_grid