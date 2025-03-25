"""
Transforms a 3x3 input grid by applying a specific digit substitution. The
transformation maps each digit in the input grid to a corresponding output
digit according to the following rules:

3 -> 4
1 -> 5
2 -> 6
8 -> 9
5 -> 1
9 -> 8
4 -> 3

Any other digit is not changed, although none appear in the examples.
"""

import numpy as np

def transform(input_grid):
    """Applies a digit substitution cipher to the input grid."""

    # Initialize the output grid as a copy of the input grid.  We'll modify it in place.
    output_grid = np.copy(input_grid)

    # Define the substitution mapping.
    substitution_map = {
        3: 4,
        1: 5,
        2: 6,
        8: 9,
        5: 1,
        9: 8,
        4: 3,
    }

    # Iterate through the grid and apply the substitution.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Apply the mapping if the digit is in the substitution map.
            if output_grid[i, j] in substitution_map:
                output_grid[i, j] = substitution_map[output_grid[i, j]]

    return output_grid