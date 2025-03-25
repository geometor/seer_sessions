"""
Transforms an input grid by duplicating each cell horizontally and vertically, then adding a border of zeros.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed pattern.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_array = np.array(input_grid)
    rows, cols = input_array.shape

    # 1. Horizontal Duplication
    expanded_h = np.repeat(input_array, 2, axis=1)

    # 2. Vertical Duplication
    expanded_v = np.repeat(expanded_h, 2, axis=0)

    # 3. Add Border
    output_rows = rows * 2 + 2
    output_cols = cols * 2 + 2
    output_array = np.zeros((output_rows, output_cols), dtype=int)
    output_array[1:-1, 1:-1] = expanded_v

    return output_array.tolist()