"""
1.  **Replication:** The 3x2 input grid is replicated four times in the output grid, without rotation or mirroring. These copies are placed to form a larger rectangular shape. The top-left corner of the input grid becomes the top-left corner of each replicated grid. The replications are positioned at coordinates (0,0), (0,2), (6,0), and (6,2) within the 9x4 output grid.

2.  **Inner Filling:**
    * Check if there exists a 2x2 square of the same non-zero color within the *input* grid.
    * If such a square is found, the 3x2 area at the center of the four replications in the output grid is filled with that same color. This area has top-left corner at (3,1) of output.
    * If there are no 2x2 squares, find non-zero color from input grid. Fill with that.

3.  **Output Grid Size:** The output grid has dimensions of 9x4.

4.  **Zero Padding:** The output grid is initialized with zeros. Any remaining pixels not filled by replication or the inner filling step retain their initial zero value.
"""

import numpy as np

def find_2x2_square(grid):
    """Checks for a 2x2 square of the same non-zero color."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            color = grid[r, c]
            if color != 0 and (grid[r:r+2, c:c+2] == color).all():
                return color
    return 0

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 4), dtype=int)

    # replicate input into the corners of output
    output_grid[0:3, 0:2] = input_grid
    output_grid[0:3, 2:4] = input_grid
    output_grid[6:9, 0:2] = input_grid
    output_grid[6:9, 2:4] = input_grid

    # find the non-zero color for inner filling
    fill_color = find_2x2_square(input_grid)

    if fill_color == 0:
      non_zero_indices = np.nonzero(input_grid)
      if len(non_zero_indices[0]) > 0 :
        fill_color = input_grid[non_zero_indices[0][0], non_zero_indices[1][0]]


    # fill the inner rectangle
    if fill_color != 0:
        output_grid[3:6, 1:3] = fill_color

    return output_grid