"""
The 6x3 input grid is reduced into a 3x3 output grid. The upper subgrid dictates the output colors, maroon (9) becomes red(2). The lower subgrid is discarded.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 6x3 input grid into a 3x3 output grid based on color mapping of the upper subgrid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Initialize an empty 3x3 output grid filled with white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Process the upper subgrid (first 3 rows).
    for i in range(3):
        for j in range(3):
            if input_array[i, j] == 9:  # If the cell is maroon (9)
                output_grid[i, j] = 2  # Change it to red (2)
            elif input_array[i,j] == 0:
                output_grid[i,j] = 0
            # else leave as default value (0)

    return output_grid.tolist()