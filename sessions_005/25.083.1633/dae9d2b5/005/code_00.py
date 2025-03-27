"""
1. **Preserve Dimensions:** Create a copy of the input grid. This copy will become the output grid, ensuring the same dimensions.
2. **Iterate:** Go through each pixel of the *copied* input grid (the output grid).
3. **Color Substitution:**
    *   If a pixel is yellow (4), change it to magenta (6).
    *   If a pixel is green (3), change it to magenta (6).
    *   If a pixel is any other color (specifically white (0) in these examples), leave it unchanged.
4.  The modified copy is the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by replacing yellow (4) and green (3) pixels with magenta (6).
    The output grid has the same dimensions as the input grid.
    """
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the output grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Perform color substitution.
            if output_grid[i, j] == 4:  # Yellow
                output_grid[i, j] = 6  # Magenta
            elif output_grid[i, j] == 3:  # Green
                output_grid[i, j] = 6  # Magenta
            # Otherwise, leave the pixel unchanged (white and other colors)

    return output_grid