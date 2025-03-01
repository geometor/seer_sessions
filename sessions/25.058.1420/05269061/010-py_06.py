"""
The transformation rule is as follows:
1. Create an output grid of the same dimensions as the input grid.
2. Disregard the input grid's values.
3. Fill the output grid with a repeating 1, 2, 4 pattern in a checkerboard style.
    - Start with '2' in the top-left corner.
    - If (row + col) is even: fill with the next in the pattern.
    - If (row + col) is odd: fill with the previous in the pattern.

"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed pattern."""

    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    pattern = [1, 2, 4]
    pattern_index = 0

    # Iterate over the grid and apply the pattern
    for row in range(rows):
        for col in range(cols):
            if (row + col) % 2 == 0:
                if (row + col) == 0:
                  output_grid[row,col] = 2 #first item
                else:
                  pattern_index = (pattern_index + 1) % len(pattern)
                  output_grid[row, col] = pattern[pattern_index]
            else:
                pattern_index = (pattern_index -1 ) % len(pattern)
                output_grid[row, col] = pattern[pattern_index]

    return output_grid