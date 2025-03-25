"""
Transforms an input grid based on the following rules:

1. Object Identification: Locate all blue (1), orange (7), azure (8), and magenta (6) pixels, and all 2x2 green (3) squares.
2. Blue Pixel Extension: If a 2x2 green square exists anywhere, extend blue downwards in columns.  For each column with blue, find the lowest blue, extend down, stopping at non-empty cells or boundary.
3. Orange Pixel Duplication: Duplicate orange (7) pixels one cell to the right if the adjacent right cell is empty (0).
4. Azure Pixel Duplication: Duplicate azure (8) pixels one cell to the left if the adjacent left cell is empty (0).
5. Magenta Pixel Movement:
    - For each magenta (6) pixel:
        - Check for any 2x2 green (3) square below in the same/overlapping columns.
        - If green is found, move magenta to the highest empty (0) cell above in the same column.
        - Overwrite the original position with 0.
"""

import numpy as np

def find_objects(grid, color):
    """Finds all instances of a specified color in the grid."""
    return np.argwhere(grid == color)

def find_2x2_squares(grid, color):
    """Finds all 2x2 squares of a specified color."""
    rows, cols = grid.shape
    squares = []
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r, c] == color and grid[r + 1, c] == color and
                grid[r, c + 1] == color and grid[r + 1, c + 1] == color):
                squares.append((r, c))  # Top-left corner
    return squares

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # 1. Object Identification
    blue_pixels = find_objects(input_grid, 1)
    orange_pixels = find_objects(input_grid, 7)
    azure_pixels = find_objects(input_grid, 8)
    magenta_pixels = find_objects(input_grid, 6)
    green_squares = find_2x2_squares(input_grid, 3)

    # 2. Blue Pixel Extension (Conditional)
    if green_squares:  # Only extend if there are green squares anywhere
        for c in range(cols):  # Iterate through all columns
            blue_in_col = False
            lowest_blue_row = -1
            for r in range(rows):
                if output_grid[r, c] == 1:
                    blue_in_col = True
                    lowest_blue_row = max(lowest_blue_row, r)  #Find lowest

            if blue_in_col: # Extend down from the lowest blue pixel
                for r in range(lowest_blue_row + 1, rows):
                    if output_grid[r, c] == 0:
                        output_grid[r, c] = 1
                    else:
                        break  # Stop at non-empty cell

    # 3. Orange Pixel Duplication (Conditional)
    for r, c in orange_pixels:
        if c + 1 < cols and output_grid[r, c + 1] == 0:
            output_grid[r, c + 1] = 7

    # 4. Azure Pixel Duplication (Conditional)
    for r, c in azure_pixels:
        if c - 1 >= 0 and output_grid[r, c - 1] == 0:
            output_grid[r, c - 1] = 8

    # 5. Magenta Pixel Movement (Conditional)
    for r, c in magenta_pixels:
        has_green_below = False
        for green_r, green_c in green_squares:
            # Check if green square is below and in same or overlapping column
            if green_r > r and (green_c == c or green_c + 1 == c or green_c == c-1 ): #Corrected Column Check
                has_green_below = True
                break

        if has_green_below:
            # Find highest empty cell above
            new_r = r
            for check_r in range(r - 1, -1, -1):
                if output_grid[check_r, c] == 0:
                    new_r = check_r
                else:
                    break  # Stop at first non-empty cell going upwards
            if new_r != r: #Only do the swap if a valid empty spot exists
              output_grid[new_r, c] = 6  # Move magenta
              output_grid[r, c] = 0  # Clear original position

    return output_grid