"""
The program takes the third number (index 2) of the first row in the input grid and uses that value for all cells of the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Select the color value from the third element (index 2) of the input grid's first row.
    selected_color = input_grid[0, 2]

    # Populate the output grid with the selected color.
    output_grid[:] = selected_color

    return output_grid