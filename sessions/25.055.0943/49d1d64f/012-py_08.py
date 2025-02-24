"""
1.  **Determine Output Dimensions:** Create a new, empty output grid. The height of the output grid is the height of the input grid plus 2. The width of the output grid is the width of the input grid plus 2.
2.  **Pad with White:** Fill the entire output grid with white pixels (color 0).
3.  **Iterate and Duplicate Rows**: For each row in the input grid:
    *   Copy the row from the input grid into the output grid, starting one row down and one column to the right (to account for the white border).
    *   Copy this same row *again* immediately below the row just copied.
"""

import numpy as np

def transform(input_grid):
    # Determine Output Dimensions
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows + 2
    output_cols = input_cols + 2

    # Pad with White
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate and Duplicate Rows
    row_index = 1 # Start one row down to account for padding
    for i in range(input_rows):
        # Copy the row
        output_grid[row_index, 1:output_cols-1] = input_grid[i]
        row_index += 1
        # Duplicate the row
        output_grid[row_index, 1:output_cols-1] = input_grid[i]
        row_index += 1


    return output_grid