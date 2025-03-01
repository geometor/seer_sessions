"""
1.  **Locate Green:** Find the location (row, column) of the single green (3) pixel within the input grid.
2.  **Determine Output Dimensions:** The output grid's height is half the input grid's height. The width stays the same.
3.  **Transform Green to Red:** Create a new grid (the output grid) of the dimensions calculated in Step 2, filled initially with white (0). In the output grid, place a red (2) pixel at the (input green row // 2 , input green column).
"""

import numpy as np

def find_green_pixel(grid):
    """Finds the coordinates of the green pixel in the grid."""
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 3:
                return row_index, col_index
    return None  # Should not happen based on problem description, but good practice

def transform(input_grid):
    # Determine Output Dimensions
    input_height, input_width = input_grid.shape
    output_height = input_height // 2
    output_width = input_width

    # Initialize output_grid with all zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Locate Green pixel
    green_row, green_col = find_green_pixel(input_grid)

    # Transform Green to Red at the calculated position
    if green_row is not None:  # Ensure green pixel was found
        output_grid[green_row // 2, green_col] = 2

    return output_grid