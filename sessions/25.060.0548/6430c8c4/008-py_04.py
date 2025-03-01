"""
The transformation rule appears to involve identifying specific colored regions
in the input grid and representing them with a single pixel of a different
color in a smaller output grid. The positions in the output grid seem to be
related to the original positions in some way. Orange (7) becomes green (3),
while all other input is set to zero.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros, sized 4x4
    output_grid = np.zeros((4, 4), dtype=int)

    # Check for the top-left 2x2 orange block (7s)
    if input_grid.shape[0] >= 2 and input_grid.shape[1] >= 2: #make sure dimensions are big enough
      if np.all(input_grid[0:2, 0:2] == 7):
          output_grid[0, 2] = 3

      #Check of top-right orange block (7s)
      if np.all(input_grid[0:2, 3] == 7):
          output_grid[1,0] = 3

    return output_grid