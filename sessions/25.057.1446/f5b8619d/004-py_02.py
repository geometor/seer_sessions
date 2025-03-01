"""
Expands a 3x3 input grid into a 6x6 output grid. Each cell in the input grid is replaced by a 2x2 block based on its color: red (2) becomes [[2, 8], [8, 2]], white (0) becomes [[0, 0], [0, 0]], orange (7) becomes [[7, 7], [7, 7]], and blue (1) becomes [[1, 1], [1, 1]].
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros((6, 6), dtype=int)

    # Iterate through each cell of the input grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Define the 2x2 replacement block based on input cell value
            if input_grid[i, j] == 2:
                block = np.array([[2, 8], [8, 2]])
            elif input_grid[i, j] == 0:
                block = np.array([[0, 0], [0, 0]])
            elif input_grid[i, j] == 7:
                block = np.array([[7, 7], [7, 7]])
            elif input_grid[i,j] == 1:
                block = np.array([[1,1], [1,1]])

            # Place the 2x2 block into the output grid
            output_grid[2*i:2*i+2, 2*j:2*j+2] = block

    return output_grid.tolist()