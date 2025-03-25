"""
Iterate through each column. Collect all non-zero elements, preserving their original order. Place these collected elements at the bottom of their respective columns in the output grid. Finally fill all remaining empty cells with zeros.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by moving non-zero elements to the bottom of each column,
    maintaining their original order, and filling the remaining cells with zeros.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through each column
    for j in range(cols):
        # Collect non-zero elements in the current column
        non_zero_elements = []
        for i in range(rows):
            if input_grid[i, j] != 0:
                non_zero_elements.append(input_grid[i, j])

        # Place the collected elements at the bottom of the column in the output grid
        for i in range(len(non_zero_elements)):
            output_grid[rows - len(non_zero_elements) + i, j] = non_zero_elements[i]

    return output_grid.tolist()