"""
1.  **Initialization:** Start with a 3x3 input grid.
2.  **Value Mapping:** For each pixel in the input grid:
    *   If the pixel's value is 0, change it to 3.
    *   If the pixel's value is 5, change it to 4.
    *   All other values are changed to 2, although in this specific example there are no other values.
3.  **Output:** The resulting 3x3 grid is the output.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified mapping rules."""
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Apply the value mapping.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 3
            elif output_grid[i, j] == 5:
                output_grid[i, j] = 4
            else:
                output_grid[i,j] = 2

    return output_grid