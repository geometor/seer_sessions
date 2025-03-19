"""
1.  **Identify Vertical '5' Columns:** Find all contiguous vertical columns of '5's.
2.  **Top Modification:** For each '5' column that extends to the row immediately above the center row, change *all* adjacent '0's *above* that column to '1'.
3.  **Center Modification:** If a '5' appears in the row immediately above the center, and also on the center row, change adjacent '0' pixels in either row to the right of that five to '2'.
4.  **Bottom Modification:** For each '5' column that extends to the bottom row *and does not* reach the center row, change the bottom-most adjacent '0' *below* that column to '3'.
5.  **All Other Pixels:** Retain their original values.
"""

import numpy as np

def find_vertical_5_columns(grid):
    """Finds all contiguous vertical columns of 5s."""
    rows, cols = grid.shape
    columns = []
    for c in range(cols):
        current_column = []
        for r in range(rows):
            if grid[r, c] == 5:
                current_column.append((r, c))
            elif current_column:
                columns.append(current_column)
                current_column = []
        if current_column:  # Handle columns that extend to the bottom
            columns.append(current_column)
    return columns

def get_adjacent_zeros(grid, r, c):
    """Finds adjacent '0's to a given cell."""
    rows, cols = grid.shape
    adjacent_zeros = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
            adjacent_zeros.append((nr, nc))
    return adjacent_zeros

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    mid_row = rows // 2

    # Find Vertical '5' Columns
    vertical_5_columns = find_vertical_5_columns(input_grid)

    # Top and Bottom Modification
    for column in vertical_5_columns:
        top_row = column[0][0]
        bottom_row = column[-1][0]
        col_index = column[0][1]

        if bottom_row >= mid_row -1 and top_row <= mid_row-1: # Extends to center
            for r in range(top_row):
                if input_grid[r, col_index] == 0:
                   output_grid[r, col_index] = 1
        elif bottom_row == rows - 1:  # Extends to bottom, but not center
                if input_grid[bottom_row,col_index] == 5:
                    for r in range(rows-1, mid_row-1, -1):
                         if input_grid[r,col_index] == 0:
                            output_grid[r,col_index]=3
                            break;


    # Center Modification
    for c in range(cols - 1):  # Iterate up to the second-to-last column
        if input_grid[mid_row - 1, c] == 5 and input_grid[mid_row,c] == 5:
            if input_grid[mid_row-1, c+1] == 0:
                output_grid[mid_row - 1, c + 1] = 2
            if input_grid[mid_row, c+1] == 0:
                output_grid[mid_row, c + 1] = 2

    return output_grid