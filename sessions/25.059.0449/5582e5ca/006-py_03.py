"""
The transformation rule is: If the input grid contains *any* yellow pixels, create an output grid of the *same dimensions* that is entirely filled with yellow. If there are no yellow pixels present, it is unclear what the output should be, since all given examples *do* have yellow.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input_grid
    output_grid = np.zeros_like(input_grid)

    # Check for the presence of yellow (4) in the input_grid
    if np.any(input_grid == 4):
        # If yellow is present, fill the output_grid with yellow
        output_grid[:] = 4

    return output_grid