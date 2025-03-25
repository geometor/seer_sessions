"""
1. Identify: Locate all pixels within the input grid that have a value of either 5 (gray) or 8 (azure).
2. Swap: If a pixel has a value of 5, change it to 8. If a pixel has a value of 8, change it to 5.
3. Preserve: All other pixels (those not having values of 5 or 8) remain unchanged from the input grid to the output grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by swapping 5s and 8s."""

    input_grid = np.array(input_grid)  # Use numpy for easier manipulation
    output_grid = np.copy(input_grid)  # Start with a copy

    # Iterate through all pixels
    rows, cols = input_grid.shape
    for row in range(rows):
        for col in range(cols):
            # Swap 5 and 8
            if input_grid[row, col] == 5:
                output_grid[row, col] = 8
            elif input_grid[row, col] == 8:
                output_grid[row, col] = 5

    return output_grid.tolist()