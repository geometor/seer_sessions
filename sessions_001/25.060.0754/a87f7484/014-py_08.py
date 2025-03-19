"""
The output is always a 3x3 grid. If orange (7) is present anywhere in the input grid, the output grid is a checkerboard pattern of orange and white, starting with orange in the top-left corner. If orange is not present in the input, the output grid is all white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid to 3x3, all white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Check for orange (7) in the input grid
    orange_present = 7 in input_grid

    # Fill output based on presence of orange
    if orange_present:
        # Checkerboard pattern
        for i in range(3):
            for j in range(3):
                if (i + j) % 2 == 0:
                    output_grid[i, j] = 7
    else:
        # All pixels remain white (0)
        pass

    return output_grid