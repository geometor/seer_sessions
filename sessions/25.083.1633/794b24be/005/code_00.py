"""
Transforms an input grid (containing 0s and 1s) to an output grid (containing 0s and 2s)
based on the following rule:
1. All occurrences of the value '1' within the input grid are replaced with the value '2'.
2. If a row in the *output* grid has the value '2', expand that row to be filled with '2's. The shape changes.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    # Initialize output as a copy, then convert 1s to 2s
    output_grid = np.copy(input_grid).astype(int)
    output_grid[output_grid == 1] = 2

    # Create a new output grid with potentially expanded shape.
    new_output = []
    for row in output_grid:
      if 2 in row:
        new_output.append([2] * 3)
      else:
         new_output.append([0] * 3)

    return np.array(new_output)