"""
The transformation rule is as follows:
1. Identify all blue pixels (value '1') in the input grid.
2. Determine how many blue pixels exists. Let this number to n
3. Create a sequence of n coordinates on the first row, starting with the coordinate (0,0) incrementing the column number each step. For example, it blue has 2 pixels, create the sequence: (0,0), (0,1)
4. Change the color of the identified pixels in that sequence to Red
5. The output grid maintains the dimensions, and any original white pixels in input will remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of all blue pixels (value '1').
    blue_pixels = np.argwhere(input_grid == 1)
    num_blue_pixels = len(blue_pixels)
    
    # set all output pixels to white
    output_grid[:] = 0

    # Create red pixels in the output grid.
    for i in range(num_blue_pixels):
        if i < output_grid.shape[1]:  # Ensure we don't go out of bounds
          output_grid[0, i] = 2

    return output_grid