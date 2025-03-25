"""
1.  **Input Replication:** The 3x2 input grid is replicated four times in the output grid, at the four corners, to create the outline of a larger rectangle. No mirroring or flipping occurs.
2. **Inner Fill:**
     *    If there are 2 pixels of non-zero color in the input that make a vertical or horizontal line segment, the inner fill is zeros.
     *    If the 2 pixels are positioned diagonally to each other, the inner fill is zeros.
     *     If a 2x2 area in the input grid is filled with the non zero color, the corresponding rectangle between the four input copies is filled with the non-zero color.

3.  **Output Size:** The output grid is always 9x4.
4. **Zero Padding:** fill the spaces outside the rectangle defined by the 4 input copies with zero.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 4), dtype=int)

    # repeat input into the corners of output
    output_grid[0:3, 0:2] = input_grid
    output_grid[0:3, 2:4] = input_grid
    output_grid[6:9, 0:2] = input_grid
    output_grid[6:9, 2:4] = input_grid

    # find the non-zero color
    non_zero_indices = np.nonzero(input_grid)
    non_zero_color = input_grid[non_zero_indices[0][0], non_zero_indices[1][0]] if len(non_zero_indices[0]) > 0 else 0

    # Determine the fill pattern based on the arrangement of colored pixels
    if non_zero_color != 0:
        # Get coordinates of non-zero pixels
        coords = np.array(np.where(input_grid == non_zero_color)).T

        # Check for 2x2 filled square
        if len(coords) == 4:
           is_square = (
               (coords[0][0] == coords[1][0] and coords[2][0] == coords[3][0] and coords[0][1] == coords[2][1] and coords[1][1] == coords[3][1]) or
               (coords[0][0] == coords[2][0] and coords[1][0] == coords[3][0] and coords[0][1] == coords[1][1] and coords[2][1] == coords[3][1]) or
               (coords[0][0] == coords[3][0] and coords[1][0] == coords[2][0] and coords[0][1] == coords[1][1] and coords[2][1] == coords[3][1])
           ) and (abs(coords[0][0] - coords[3][0]) ==1) and (abs(coords[0][1]-coords[3][1])==1)

        else:
          is_square = False

        if is_square:
            # Fill the inner rectangle
            output_grid[3:6, :] = non_zero_color
        else:
          # Check the relative positions for filling the inner rectangle between input replications
          if len(coords) >= 2: #fill space between replications, cases for 8 and 5
            output_grid[3:6, 0:2] = 0
            output_grid[3:6, 2:4] = 0

    return output_grid