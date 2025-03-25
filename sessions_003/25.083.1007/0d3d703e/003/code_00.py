"""
The transformation performs a digit substitution on the input grid. The following substitutions are applied:

*   3 becomes 4
*   1 becomes 5
*   2 becomes 6
*   8 becomes 9
*   5 becomes 1
*   9 becomes 8
*   4 becomes 3
*   6 becomes 2

All other digits remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """Applies a digit substitution cipher to the input grid."""

    # Initialize the output grid as a copy of the input grid.  We'll modify it in place.
    output_grid = np.copy(input_grid)

    # Define the complete substitution mapping.
    substitution_map = {
        3: 4,
        1: 5,
        2: 6,
        8: 9,
        5: 1,
        9: 8,
        4: 3,
        6: 2,  # Add the missing mapping from the analysis
    }

    # Iterate through the grid and apply the substitution.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Apply the mapping if the digit is in the substitution map.
            if output_grid[i, j] in substitution_map:
                output_grid[i, j] = substitution_map[output_grid[i, j]]

    return output_grid