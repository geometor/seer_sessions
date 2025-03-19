"""
The input grid is transformed into a smaller 1D output grid.
The transformation extracts a summary of the presence of blue pixels (color 1)
in each row of the input grid. If a row in input grid has a blue pixel, it
will have one in the output array. Fill rest of the array with white.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 2D input grid into a 1D output grid representing presence
    of at least one blue (1) pixel in each row.
    """
    input_grid = np.array(input_grid)
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Count the number of blue pixels (value 1) in the current row
        blue_count = np.count_nonzero(row == 1)

        # if blue > 0, then 1
        if blue_count > 0:
            output_grid.append(1)

    # Pad the output array with white pixels (0) until its length is 5.
    while len(output_grid) < 5:
        output_grid.append(0)

    return output_grid