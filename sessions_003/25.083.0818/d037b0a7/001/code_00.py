"""
1.  **Identify Sources:** Find all non-zero values in the top row of the input grid. These are the "source" values.

2.  **Column-wise Propagation:** For each source value:
    *   Iterate down the column starting from the top row.
    *   If the current cell is 0, replace it with the source value.
    *    If it is not zero, the source value changes to it.

3.  **Output:** The modified grid is the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column
    for j in range(cols):
        # Find the source value in the top row of the current column
        source_value = input_grid[0, j]

        # Propagate the source value downwards
        for i in range(rows):
            if output_grid[i,j] == 0:
                output_grid[i, j] = source_value
            else:
                source_value = output_grid[i,j]

    return output_grid