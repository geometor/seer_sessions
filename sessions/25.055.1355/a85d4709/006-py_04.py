"""
1.  **Input:** Begin with an input grid of any size.
2.  **Transformation:** For *every* pixel in the input grid:
    *   Change a value of 0 to 3.
    *   Change a value of 1 to 2.
    *   Change a value of 2 to 1.
    *   Change a value of 5 to 4.
    *   All other values are unchanged
3.  **Output:** The result of these value substitutions is the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # change output pixels based on the mapping rules
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 3
            elif output_grid[i, j] == 1:
                output_grid[i, j] = 2
            elif output_grid[i, j] == 2:
                output_grid[i, j] = 1
            elif output_grid[i, j] == 5:
                output_grid[i, j] = 4

    return output_grid