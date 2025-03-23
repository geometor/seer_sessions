"""
The transformation rule is a horizontal flip. For each row in the input grid, the order of elements is reversed. The element at `input[row][col]` is moved to `output[row][N-1-col]`, where `N` is the number of columns in the grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by flipping each row horizontally.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Flip each row horizontally using NumPy's fliplr function.
    output_array = np.fliplr(input_array)

    # Convert the output NumPy array back to a list.
    output_grid = output_array.tolist()
    return output_grid