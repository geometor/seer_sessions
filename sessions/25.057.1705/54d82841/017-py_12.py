"""
Copies the input grid and appends a new row. The color of each pixel in the new row 
depends on the colors present in the corresponding column of the input grid. If a 
column contains any color other than black (0) or white(0), the corresponding pixel 
in the new row is yellow (4); otherwise, it's black (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid).tolist()
    
    # Append a new row.  Initialize it to all black.
    num_cols = len(input_grid[0])
    new_row = [0] * num_cols
    output_grid.append(new_row)

    # Iterate through each column of the input grid
    for col_index in range(num_cols):
        # Get unique colors in the current column, excluding 0 (black)
        column_colors = np.unique(input_grid[:, col_index])
        non_black_white_exists = False
        for color in column_colors:
            if color != 0:
              non_black_white_exists = True
              break

        # If a non-black, non-white color exists in this column, set the corresponding pixel in new row to yellow (4)
        if non_black_white_exists:
            output_grid[-1][col_index] = 4
        # otherwise the value is already 0, as initialized

    return np.array(output_grid)