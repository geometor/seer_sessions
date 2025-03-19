"""
Transforms an input grid with a vertical orange line into an output grid with an expanded pattern of orange and azure pixels.
The transformation creates a checkered pattern of orange and azure, originating from the orange line in the input grid and expanding
to the right.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed pattern.
    """
    output_grid = np.copy(input_grid)  # Initialize output grid as a copy of the input
    rows, cols = input_grid.shape

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Check for orange pixels (the starting line)
            if input_grid[r, c] == 7:
                output_grid[r, c] = 7  # Keep the original orange pixel
                # Expand the checkered pattern to the right
                for i in range(1, cols - c):
                    if (c + i) < cols:
                        if i % 2 == 1:  # Odd columns are azure
                            output_grid[r, c + i] = 8
                        else:  # Even columns are orange
                            output_grid[r, c + i] = 7
    return output_grid