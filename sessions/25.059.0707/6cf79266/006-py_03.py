"""
Finds a 3x3 square of uniform color within the input grid and replaces it with a 3x3 square of a different, specific color. The replacement color is determined by the row where the 3x3 square starts: row index 5->red, 6->yellow, 7->azure.
"""

import numpy as np

def find_3x3_square(grid):
    # Iterate through the grid to find a 3x3 square.
    rows, cols = grid.shape
    for i in range(rows - 2):
        for j in range(cols - 2):
            # Extract the 3x3 region.
            subgrid = grid[i:i+3, j:j+3]
            # Check if all elements in the subgrid are the same.
            if np.all(subgrid == subgrid[0, 0]):
                return i, j, subgrid[0, 0]  # Return row, col, and color
    return None, None, None  # No 3x3 square found

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)

    # Find the starting position and color of a 3x3 square.
    row_start, col_start, color = find_3x3_square(input_grid)

    if row_start is not None:
        # Determine the replacement color based on the starting row.
        if row_start == 5:
          replacement_color = 2  # Red
        elif row_start == 6:
          replacement_color = 4 # Yellow
        elif row_start == 7:
          replacement_color = 8 # Azure
        else:
          replacement_color = color # default is no change, should not happen

        # Replace the 3x3 square with the new color.
        output_grid[row_start:row_start + 3, col_start:col_start + 3] = replacement_color

    return output_grid