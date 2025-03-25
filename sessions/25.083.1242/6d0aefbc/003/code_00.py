"""
The transformation rule is: For each column in the input grid, create an identical copy of that column.  The output grid consists of each original input column immediately followed by its duplicate. The width of the output grid is twice the width of the input grid, and the height remains the same. The order of columns from left to right is preserved and duplicated.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating each column.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * 2), dtype=int)

    # Iterate through the columns of the input grid.
    for i in range(input_grid.shape[1]):
        # Copy each column to its corresponding position in the output grid.
        output_grid[:, 2*i] = input_grid[:, i]
        output_grid[:, 2*i + 1] = input_grid[:, i]

    return output_grid.tolist()