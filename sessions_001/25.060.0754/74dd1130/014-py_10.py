"""
The transformation swaps vertically adjacent magenta (6) and red (2) pixels. If a magenta pixel is directly above a red pixel, their positions are swapped in the output grid. This operation is applied to the entire grid, considering all such pairs.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each pixel of the input grid
    for r in range(rows - 1):  # Iterate up to the second-to-last row
        for c in range(cols):
            # Check if the current pixel and the one below it are magenta and red, or vice-versa
            if (output_grid[r, c] == 6 and output_grid[r + 1, c] == 2) or \
               (output_grid[r, c] == 2 and output_grid[r + 1, c] == 6):
                # Swap the pixels
                temp = output_grid[r, c]
                output_grid[r, c] = output_grid[r + 1, c]
                output_grid[r + 1, c] = temp
    return output_grid