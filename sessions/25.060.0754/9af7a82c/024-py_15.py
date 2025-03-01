"""
The program copies the input grid to the output. Then, it iterates through specific color values (7, 8, 6, 1 in that order) to potentially append rows.  For each of these colors, it checks each column. If the color exists in the column, a new row is appended to the output.  This new row is filled with zeros, except for the current column index, where the value is set to the color being checked. The rows are added in order 7, 8, 6, and 1.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()

    # change output pixels
    colors_to_check = [7, 8, 6, 1]
    for color in colors_to_check:
        for col in range(input_grid.shape[1]):
            if color in input_grid[:, col]:
                new_row = np.zeros(input_grid.shape[1], dtype=int)
                new_row[col] = color
                output_grid = np.vstack([output_grid, new_row])

    return output_grid.tolist()