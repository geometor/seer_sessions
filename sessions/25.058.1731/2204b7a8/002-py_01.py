"""
Transforms the input grid based on the following rule:
Interior pixels above the main diagonal are changed to the top border color, 
and interior pixels below the main diagonal are changed to the bottom border color.
Border colors remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Determine top and bottom border colors
    top_border_color = output_grid[0, 0]
    bottom_border_color = output_grid[-1, 0]

    # Iterate through interior pixels
    for i in range(1, rows - 1):
        for j in range(cols):
            # Check diagonal relationship and change color accordingly
            if i < j:  # Above main diagonal
                output_grid[i, j] = top_border_color
            elif i > j:  # Below main diagonal
                output_grid[i, j] = bottom_border_color
            # else on main diagonal, do nothing

    return output_grid