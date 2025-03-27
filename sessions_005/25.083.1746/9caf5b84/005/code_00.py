"""
Iterate through each pixel of the input grid. For each pixel, check if it has any
neighbors with a different color or is on the grid edge. If it does,
change the color of the pixel to orange (7) in the output grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in the grid."""
    rows, cols = len(grid), len(grid[0])
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            new_row, new_col = row + i, col + j
            if 0 <= new_row < rows and 0 <= new_col < cols:
                neighbors.append((new_row, new_col))
    return neighbors

def is_outer_border(grid, row, col):
    """Checks if a pixel is on the outer border of a contiguous region."""
    rows, cols = len(grid), len(grid[0])
    current_color = grid[row][col]
    neighbors = get_neighbors(grid, row, col)

    # Check if the pixel is on the edge of the grid
    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
        return True

    # Check if any neighbor has a different color
    for neighbor_row, neighbor_col in neighbors:
        if grid[neighbor_row][neighbor_col] != current_color:
            return True

    return False

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = len(input_grid), len(input_grid[0])

    # Iterate through each cell and check if it's on the border
    for row in range(rows):
        for col in range(cols):
            if is_outer_border(input_grid, row, col):
                output_grid[row][col] = 7

    return output_grid