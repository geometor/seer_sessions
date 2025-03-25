"""
1.  **Locate Key Pixels:** Find the single azure ('8') pixel and the single orange ('7') pixel in the input grid. Note their row and column indices.
2.  **Calculate:**
    *   `rows_above`: The number of rows above the azure pixel.
    *   `rows_below`: The number of rows below the azure pixel.
    *    `separation`: The horizontal distance (number of columns) between the azure and orange pixels (column index of orange - column index of azure).
3.  **Create Base Row:** Extract the section of the row that goes from the azure pixel to the orange pixel (inclusive).
4.  **Vertical Expansion:**
    - Duplicate the base row `rows_above` times *above* the original azure pixel's row.
    - Duplicate the base row `rows_below` times *below* the original azure pixel's row, *including* duplicating the original row containing the azure and orange.
5. **Extend Regions:**
    - Find the position of 8 in the original row. Extend all 8s to the left edge of the grid.
    - Find the position of 7 in the original row. Extend all 7s to the right edge of the grid.
6.  **Insert Red Diagonal:**
    *   Starting Point:  The red diagonal starts in the row immediately below the last row of the upper duplicated section (at row index `rows_above`) and at column equal to the original column index of the '7'.
    *   Traversal: Move one row down and one column to the left with each step, placing a red ('2') pixel.
    *   Stopping Condition: Stop adding red pixels when you reach the row which contains the original base row.
"""

import numpy as np

def find_pixels(grid, pixel_values):
    """Finds the coordinates of specified pixels in the grid."""
    coords = {}
    for value in pixel_values:
        coords[value] = []
        for r, row in enumerate(grid):
            for c, pixel in enumerate(row):
                if pixel == value:
                    coords[value].append((r, c))
    return coords

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # 1. Locate Key Pixels
    pixel_coords = find_pixels(input_grid, [7, 8])
    eight_coord = pixel_coords[8][0]
    seven_coord = pixel_coords[7][0]
    row_8, col_8 = eight_coord
    row_7, col_7 = seven_coord

    # 2. Calculate
    rows_above = row_8
    rows_below = input_grid.shape[0] - row_8 - 1
    separation = col_7 - col_8

    # 3. Create Base Row
    base_row = input_grid[row_8, col_8:col_7+1]

    # 4. Vertical Expansion
    row_insert = 0
    for i in range(rows_above):
        output_grid[row_insert, col_8:col_7+1] = base_row
        row_insert += 1
    
    # include original
    output_grid[row_insert, col_8:col_7+1] = base_row
    row_insert += 1

    for i in range(rows_below):
        output_grid[row_insert, col_8:col_7+1] = base_row
        row_insert += 1

    # 5. Extend Regions
    for r in range(output_grid.shape[0]):
        # Extend 8s to the left
        if output_grid[r,col_8] == 8:
            for c in range(col_8):
                output_grid[r,c] = 8
        # Extend 7s to the right
        if output_grid[r, col_7] == 7:
            for c in range(col_7 + 1, output_grid.shape[1]):
                output_grid[r,c] = 7

    # 6. Insert Red Diagonal
    start_row = rows_above
    start_col = col_7
    current_row = start_row
    current_col = start_col

    while current_row <= rows_above + rows_below :
        if 0 <= current_row < output_grid.shape[0] and 0 <= current_col < output_grid.shape[1]:
            output_grid[current_row, current_col] = 2
        current_row += 1
        current_col -= 1


    return output_grid