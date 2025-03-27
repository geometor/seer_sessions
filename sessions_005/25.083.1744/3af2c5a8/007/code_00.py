"""
1.  **Double Dimensions:** The output grid's dimensions are double the input grid's dimensions (height * 2, width * 2).

2.  **Replication with Shifts:** The input grid is replicated in the output grid, but with specific row and column shifts:
    *   The top-left cell of the output grid is the same as the top left of the input
    *   The input row at index `i` is repeated on output rows `i` and `height - 1 - i`
    *   The input column at index `j` is repeated on output columns `j` and `width - 1 - j`

3.  **Combining:** combine steps to position each value from the input grid at `input[i,j]` to `output[i,j]`, `output[height - 1 - i, j]`, `output[i, width -1 - j]`, and `output[height - 1 - i, width - 1 -j]`
"""

import numpy as np

def transform(input_grid):
    # Double Dimensions
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replication with Shifts
    for i in range(input_height):
        for j in range(input_width):
            # Map input[i,j] to output[i,j], output[height - 1 - i, j], output[i, width -1 - j], and output[height - 1-i, width -1 - j]
            output_grid[i, j] = input_grid[i, j]
            output_grid[output_height - 1 - i, j] = input_grid[i, j]
            output_grid[i, output_width - 1 - j] = input_grid[i, j]
            output_grid[output_height - 1 - i, output_width - 1 - j] = input_grid[i, j]

    return output_grid