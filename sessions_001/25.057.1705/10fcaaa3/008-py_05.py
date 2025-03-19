"""
The transformation rule involves the following steps:
1. Expand the input grid by doubling its dimensions (both height and width).
2. Replicate the magenta pixels ('6') from the input grid in the output grid based on a specific pattern.
    - Each '6' in the input corresponds to a 2x2 section in the output.
    -  Within its 2x2 section, each '6' is placed in a specific, repeating pattern.
3. Fill the remaining cells with azure ('8') in a checkerboard and solid line pattern. The 8's fill the 2x2 section for the doubled pixel locations as well as perimeter lines.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate and Offset '6'
    for r in range(input_height):
        for c in range(input_width):
            if input_grid[r, c] == 6:
                output_grid[r * 2, c * 2] = 6  # Top-left
                output_grid[r * 2 + 1 , c*2 +1] = 0
                if output_grid[r*2, c*2+1] != 6:
                    output_grid[r * 2, c * 2 + 1] = 0  # Top-right, only if it hasn't already been placed.
                if output_grid[r*2+1, c*2] != 6:
                     output_grid[r * 2 + 1, c * 2] = 0 # Bottom-left only if it hasn't.

    # Fill with 8s - doing the solid line perimeter and between sections
    for r in range(output_height):
      for c in range(output_width):
          if (r%2==0 and c%2==1) or (r%2==1 and c%2==0) or (r%2==1 and c%2==1):
            output_grid[r,c] = 8

    for r in range(input_height):
        for c in range(input_width):
            if input_grid[r, c] == 6:
                output_grid[r * 2 + 1 , c*2 +1] = 0

    return output_grid