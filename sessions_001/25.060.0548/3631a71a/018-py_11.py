"""
1. Identify the Target Color: Determine the non-zero color that is present in the input grid.
2. Replace with Zero: Change all pixels of the target color to 0.
"""

import numpy as np

def _find_target_color(grid):
    # Find all unique colors in the grid.
    unique_colors = np.unique(grid)
    # Filter out 0 (background color) and return the first remaining color.
    for color in unique_colors:
        if color != 0:
            return color
    return 0  # Return 0 if no target color is found (shouldn't happen in these examples)

def transform(input_grid):
    """
    Transforms the input grid by changing all occurrences of the non-zero color to 0.
    """
    # Create a copy of the input grid to modify.
    output_grid = np.copy(input_grid)

    # Find the target color.
    target_color = _find_target_color(input_grid)

    # Iterate through each cell of the grid.
    for row_index, row in enumerate(input_grid):
        for col_index, cell_value in enumerate(row):
            # Check if the cell value is the target color.
            if cell_value == target_color:
                # Change the value to 0 in the output grid.
                output_grid[row_index][col_index] = 0

    return output_grid