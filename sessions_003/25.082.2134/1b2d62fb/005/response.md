```python
"""
Transforms an input grid by identifying cells with value '1' (markers), replacing
adjacent '0's with '8's, and then placing those '8's in a new 5x3 output grid
in a top-to-bottom, left-to-right order. All other cells in the output are '0'.
"""

import numpy as np

def get_adjacent_indices(grid, row, col):
    # Get indices of adjacent cells (up, down, left, right)
    rows, cols = grid.shape
    adjacent_indices = []
    if row > 0:
        adjacent_indices.append((row - 1, col))  # Up
    if row < rows - 1:
        adjacent_indices.append((row + 1, col))  # Down
    if col > 0:
        adjacent_indices.append((row, col - 1))  # Left
    if col < cols - 1:
        adjacent_indices.append((row, col + 1))  # Right
    return adjacent_indices

def transform(input_grid):
    # initialize output_grid as 5x3 with 0s
    output_grid = np.zeros((5, 3), dtype=int)

    # Create a temporary grid to store the 8s before placing them
    temp_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all markers (value 1)
    marker_rows, marker_cols = np.where(input_grid == 1)

    # Replace adjacent 0s with 8s in temp grid
    for marker_row, marker_col in zip(marker_rows, marker_cols):
        adjacent_indices = get_adjacent_indices(input_grid, marker_row, marker_col)
        for r, c in adjacent_indices:
            if input_grid[r, c] == 0:
                temp_grid[r, c] = 8

    # Collect the '8's in order from the modified input grid
    eights_list = []
    for r in range(rows):
        for c in range(cols):
            if temp_grid[r,c] == 8:
                eights_list.append(8)

    # Populate the output grid with the collected '8's
    output_row = 0
    output_col = 0
    for eight in eights_list:
        if output_row < 5:  # Ensure we don't go out of bounds
            output_grid[output_row, output_col] = eight
            output_col += 1
            if output_col == 3:  # Move to the next row
                output_col = 0
                output_row += 1

    return output_grid
```