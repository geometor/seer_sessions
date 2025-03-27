"""
The output is created by writing the values in the input from top to bottom into output rows from bottom to top.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule: values from top to bottom
    in the input become rows from bottom to top in the output.
    """
    input_array = np.array(input_grid)
    num_rows, num_cols = input_array.shape
    output_grid = np.zeros((num_rows, num_cols), dtype=int).tolist()

    for i in range(num_rows):
        for j in range(num_cols):
            output_grid[num_rows - 1 - i][j] = input_array[i][j]

    return output_grid