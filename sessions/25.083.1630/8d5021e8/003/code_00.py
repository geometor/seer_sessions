"""
Transforms an input grid into an output grid by expanding its dimensions. The output
grid's height is three times the input's height, and the width is two times the
input's width.  The transformation replicates and repositions input pixels in a specific pattern.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described expansion and replication rule.
    """
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_height = input_height * 3
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    for i in range(input_height):
        for j in range(input_width):
            # Place the value input[i,j] in output[i*3,j*2]
            output_grid[i * 3, j * 2] = input_grid[i, j]

            # if the j+1 is less than the width of the input grid:
            if j + 1 < input_width:
                # Place the input[i, j+1] in the output[i*3, j*2 + 1]
                output_grid[i * 3, j * 2 + 1] = input_grid[i, j+1]
                # Place the input[i, j+1] in the output[i*3 + 1, j*2 + 1]
                output_grid[i * 3 + 1, j * 2 + 1] = input_grid[i, j + 1]
            else:  # otherwise,
                # Place the input[i, j] in the output[i*3, j*2 + 1]
                output_grid[i * 3, j * 2 + 1] = input_grid[i, j]
                # Place the input[i, j] in the output[i*3 + 1, j*2 + 1]
                output_grid[i * 3 + 1, j * 2 + 1] = input_grid[i, j]
            # Place the value input[i,j] in output[i*3 + 1, j*2].
            output_grid[i * 3 + 1, j * 2] = input_grid[i, j]
            # Place the value input[i,j] in output[i*3 + 2, j*2].
            output_grid[i * 3 + 2, j * 2] = input_grid[i, j]
            # if the j+1 is less than the width of the input grid:
            if j + 1 < input_width:
                # Place the input[i, j+1] in the output[i*3 + 2, j*2 + 1]
                output_grid[i * 3 + 2, j * 2 + 1] = input_grid[i, j + 1]
            else: # otherwise,
                #  Place the input[i, j] in the output[i*3 + 2, j*2 + 1]
                output_grid[i * 3 + 2, j * 2 + 1] = input_grid[i, j]

    return output_grid.tolist()