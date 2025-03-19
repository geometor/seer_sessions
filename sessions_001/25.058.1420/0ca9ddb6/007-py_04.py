"""
1.  **Initialization:** Create a copy of the input grid to serve as the output grid.
2.  **Red Expansion:** Locate all red (value 2) pixels in the input grid. For each red pixel, change all directly and diagonally contiguous pixels (the "aura") with a value of 0 to yellow (value 4). Stop when reaching the border or a non-zero value.
3. **Blue Expansion:** Locate all blue (value 1) pixels. Fill their "aura" (contiguous zero-value region, directly or diagonally touching) with orange (value 7). Stop when the boundary or a non-zero value is hit.
"""

import numpy as np

def get_all_neighbors(grid, row, col):
    """
    Gets all 8 neighbors (including diagonals) of a cell.
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the cell itself
                neighbors.append((i, j))
    return neighbors

def flood_fill(grid, row, col, target_color, replacement_color):
    """
    Performs a flood fill, replacing contiguous target_color cells with replacement_color.
    """
    if grid[row, col] != target_color:
        return
    grid[row, col] = replacement_color
    neighbors = get_all_neighbors(grid, row, col)
    for r, c in neighbors:
        flood_fill(grid, r, c, target_color, replacement_color)

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Red Expansion
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 2:  # Red pixel
                # Perform flood fill with yellow (4) for contiguous 0s
                for r, c in get_all_neighbors(input_grid, row, col):
                    flood_fill(output_grid, r, c, 0, 4)
                output_grid[row,col] = 2 # ensure center pixel unchanged

    # Blue Expansion
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 1:  # Blue pixel
                # Perform flood fill with orange (7) for contiguous 0s
                for r, c in get_all_neighbors(input_grid, row, col):
                    flood_fill(output_grid, r, c, 0, 7)
                output_grid[row,col] = 1 # ensure center pixel unchanged

    return output_grid