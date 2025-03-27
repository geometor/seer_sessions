"""
Preserves '7's and reverse the order of the other numbers within each column.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by preserving '7's and reversing the order
    of other numbers within each column.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = [[0] * cols for _ in range(rows)]

    # Iterate through each column
    for j in range(cols):
        # Collect non-7 elements in the current column
        non_seven_elements = []
        for i in range(rows):
            if input_grid[i][j] != 7:
                non_seven_elements.append(input_grid[i][j])

        # Reverse the order of non-7 elements
        non_seven_elements.reverse()

        # Place elements back into the output grid
        k = 0  # Index for the reversed non-7 elements
        for i in range(rows):
            if input_grid[i][j] == 7:
                output_grid[i][j] = 7  # Preserve '7'
            else:
                if k < len(non_seven_elements):
                    output_grid[i][j] = non_seven_elements[k]
                    k += 1

    return output_grid