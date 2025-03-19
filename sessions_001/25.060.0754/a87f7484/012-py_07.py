"""
Examine the input grid for the presence of orange (7).
Create a 3x3 output grid.
If orange is present, fill corners and center with orange, otherwise fill with white.
If no orange, fill entire output grid with white.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to the output grid based on the presence of orange.
    """
    # Initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Check for orange (7) in the input grid
    orange_present = 7 in input_grid

    # Conditional Fill
    if orange_present:
        # Fill the corner and center pixels of output grid with orange (7)
        output_grid[0, 0] = 7
        output_grid[0, 2] = 7
        output_grid[1, 1] = 7
        output_grid[2, 0] = 7
        output_grid[2, 2] = 7
        # The rest of the pixels are already initialized to 0 (white)
    else:
        # All pixels remain 0 (white) as initialized
        pass

    return output_grid