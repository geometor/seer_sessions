"""
Transforms a 3x3 input grid based on the positions of '5' (gray) pixels to a 3x3 output grid filled with a specific color. The output color is determined by a set of rules mapping '5' locations to colors.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the positions of '5's.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = np.where(input_grid == 5)
    positions = list(zip(rows, cols))

    # Determine output color based on positions of '5'
    if (0, 0) in positions and (1, 1) in positions and len(positions) == 2:
        output_grid[:] = 2  # Red
    elif all(pos[1] == 2 for pos in positions):
        output_grid[:] = 3  # Green
    elif (1,1) in positions and (2,2) in positions and len(positions) == 2:
        output_grid[:] = 4 # Yellow
    elif (0, 2) in positions and (1, 1) in positions and (2, 0) in positions: # Top-right, Middle, Bottom-left
        output_grid[0, :] = 3  # Green
        output_grid[1, :] = 4  # Yellow
        output_grid[2, :] = 2  # Red

    else:
      output_grid[:] = 0

    return output_grid.tolist()