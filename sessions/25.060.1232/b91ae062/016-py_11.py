"""
Expands each cell in the input 3x3 grid into a 3x3 block in the output 9x9 grid, replicating the original cell's value.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid into a 9x9 output grid by expanding each cell into a 3x3 block.

    Args:
        input_grid (list of lists): The 3x3 input grid.

    Returns:
        list of lists: The 9x9 expanded output grid.
    """
    # initialize output_grid as a 9x9 array filled with zeros
    output_grid = np.zeros((9, 9), dtype=int)

    # Iterate through each cell of the input grid
    for i in range(3):
        for j in range(3):
            # Get the value of the current cell
            value = input_grid[i][j]

            # Expand the cell into a 3x3 block in the output grid
            for row in range(3 * i, 3 * (i + 1)):
                for col in range(3 * j, 3 * (j + 1)):
                    output_grid[row][col] = value

    return output_grid.tolist()