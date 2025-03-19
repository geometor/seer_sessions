"""
Replaces all instances of green (3) and red (2) with azure (8) in the input grid,
while preserving the grid structure and all other colors.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule: 3 and 2 -> 8.
    """
    output_grid = np.copy(input_grid)  # Create a copy to avoid modifying the original

    # Iterate through the grid
    for row_index, row in enumerate(input_grid):
        for col_index, cell_value in enumerate(row):
            # Check if the cell value is 3 or 2
            if cell_value == 3 or cell_value == 2:
                # Change the value to 8
                output_grid[row_index, col_index] = 8

    return output_grid