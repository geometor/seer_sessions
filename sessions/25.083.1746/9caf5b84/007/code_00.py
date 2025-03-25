"""
1.  **Identify Contiguous Regions:** For each pixel in the input grid, determine the contiguous region of pixels with the same color. A contiguous region is defined as a group of one or more pixels of the same color that are directly adjacent to each other (horizontally or vertically, but not diagonally).
2.  **Identify Border Pixels:** For each contiguous region, identify its border pixels. A border pixel is one that either:
    *   Is on the edge of the entire grid.
    *   Has at least one directly adjacent pixel (horizontally or vertically) that has a *different* color.
3.  **Transform Border Pixels:** In the output grid (initialized as a copy of the input grid), change the color of all identified border pixels to orange (7).
4. **Leave Non-Border Pixels Unchanged:** Pixels that are not part of any border should retain their original color from the input grid in the output grid.
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

    # Check if any neighbor has a different color, only consider adjacent (not diagonal)
    for neighbor_row, neighbor_col in neighbors:
        if abs(neighbor_row - row) + abs(neighbor_col - col) == 1:  # Check for direct adjacency
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