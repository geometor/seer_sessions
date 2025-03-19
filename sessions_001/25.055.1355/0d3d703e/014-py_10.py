"""
Transforms a 3x3 grid by replacing specific integer values (colors) with other integer values, effectively performing a color substitution. The mapping is: 5 -> 1, 8 -> 9, and 6 -> 2.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified color substitution rules.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Apply the color substitution rules.
    output_grid[input_grid == 5] = 1  # Replace 5 (gray) with 1 (blue)
    output_grid[input_grid == 8] = 9  # Replace 8 (azure) with 9 (maroon)
    output_grid[input_grid == 6] = 2  # Replace 6 (magenta) with 2 (red)

    return output_grid