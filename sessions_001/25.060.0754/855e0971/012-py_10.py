"""
The input grid is transformed as follows: For each row in the grid, identify the right-most white pixel. If a row contains one or more white pixels, change all red pixels to the left of that row's right-most white pixel to white. If a row does not contain any white pixels, no changes are made to that row. The colors of non-red and non-white pixels are not changed, nor does any change occur based on columns.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Find all white pixel indices in the current row
        white_indices = np.where(input_grid[r, :] == 0)[0]

        # If white pixels exist in the row
        if white_indices.size > 0:
            # Find the right-most white pixel index
            rightmost_white_index = white_indices[-1]

            # Change red pixels to white to the left of the right-most white
            for c in range(rightmost_white_index):
                if output_grid[r, c] == 2:
                    output_grid[r, c] = 0

    return output_grid