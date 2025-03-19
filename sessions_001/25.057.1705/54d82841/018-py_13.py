"""
A new row is added to the bottom of the input grid. For each column in the input grid:

1.  If *all* the pixels in the column are white (0), the corresponding pixel in the added row is yellow (4).
2. If the column contains *any* non-white pixels, and all the white pixels are above the non-white pixels, the corresponding pixel in the new row is also yellow (4).
3.  Otherwise, if the column contains any non-white pixels, where a white pixel is *not* above a non-white, the corresponding pixel in the added row is black (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    output_grid = np.copy(input_grid)
    new_row = np.zeros((1, output_grid.shape[1]), dtype=int)
    output_grid = np.vstack((output_grid, new_row))

    for j in range(input_grid.shape[1]):
        column = input_grid[:, j]
        non_white_indices = np.where(column != 0)[0]

        if len(non_white_indices) == 0:
            # All pixels are white
            output_grid[-1, j] = 4
        else:
            # Check if all white pixels are above non-white pixels
            first_non_white = non_white_indices[0]
            all_white_above = np.all(column[:first_non_white] == 0)

            if all_white_above:
                 output_grid[-1,j] = 4
            else:
                output_grid[-1, j] = 0

    return output_grid