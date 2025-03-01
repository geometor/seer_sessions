"""
The transformation performs a direct color substitution based on these rules:

1.  Replace all occurrences of gray (5) with blue (1).
2.  Replace all occurrences of azure (8) with maroon (9).
3.  Replace all occurrences of magenta (6) with red (2).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Replace all occurrences of gray (5) with blue (1).
    output_grid[input_grid == 5] = 1
    # Replace all occurrences of azure (8) with maroon (9).
    output_grid[input_grid == 8] = 9
    # Replace all occurrences of magenta (6) with red (2).
    output_grid[input_grid == 6] = 2

    return output_grid