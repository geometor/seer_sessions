"""
Iterate through the grid, and every value that is 9, changes to 0.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing all occurrences of the value 9 to 0.
    """
    # Create a copy of the input grid to modify.  This avoids modifying the original.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the grid.
    for row_index, row in enumerate(input_grid):
        for col_index, cell_value in enumerate(row):
            # Check if the cell value is 9.
            if cell_value == 9:
                # Change the value to 0 in the output grid.
                output_grid[row_index][col_index] = 0

    return output_grid