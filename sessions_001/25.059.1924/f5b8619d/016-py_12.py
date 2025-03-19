"""
The transformation rule can be described as follows:

1. **Double the Grid:** The original 2x2 input grid is doubled in both dimensions to create a 4x4 output grid.

2. **Replicate and Transform:**
   - White (0) pixels from the input grid are copied to their corresponding doubled positions in the output grid. A white pixel at (0,0) in the input becomes white pixels at (0,0), (0,2), (2,0), and (2,2) in the output.
   - For each yellow (4) pixel in the input grid:
     - A yellow pixel (4) is placed in the corresponding location in the output grid.
     - A new color, azure (8), is placed in the horizontally and vertically adjacent pixels in the output.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize the output grid as a 4x4 array filled with zeros.
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the input grid.
    for i in range(2):
        for j in range(2):
            # Copy the white pixels.
            if input_grid[i, j] == 0:
                output_grid[2*i, 2*j] = 0
                output_grid[2*i+1, 2*j] = 0
                output_grid[2*i, 2*j+1] = 0
                output_grid[2*i+1, 2*j+1] = 0
            # Transform and replicate the yellow pixels.
            elif input_grid[i, j] == 4:
                output_grid[2*i, 2*j] = 4
                output_grid[2*i+1, 2*j] = 8
                output_grid[2*i, 2*j+1] = 8
                output_grid[2*i+1, 2*j+1] = 8
    return output_grid