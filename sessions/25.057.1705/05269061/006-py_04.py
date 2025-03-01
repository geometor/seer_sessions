"""
The transformation rule is to replace all white (0) pixels in the input grid with a checkerboard pattern of red (2), azure (8), and green (3), starting with red in the top-left corner. The pattern is seeded by the presence of a 2, 8, 3 sequence in the input.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing 0s with a checkerboard pattern.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Start with a copy to preserve non-0 pixels
    pattern = [2, 8, 3]

    # Iterate through the output grid and apply the checkerboard pattern, only replacing 0s.
    for i in range(rows):
        for j in range(cols):
            if output_grid[i, j] == 0:
                output_grid[i, j] = pattern[(i + j) % 3]  # Use modulo operator
    return output_grid