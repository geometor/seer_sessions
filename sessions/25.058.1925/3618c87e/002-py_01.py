"""
The transformation rule is as follows:
1.  Identify all blue (1) pixels in the input grid.
2.  For each column containing a blue pixel:
    *   Find the gray (5) pixel at the bottom row in the same column of the output grid.
    *   Change gray pixel color to blue pixel color.
3.  All other pixels in the input that are not blue, maintain color and position in the output.
4. The pixels in the input grid that are above an identified blue, are changed to white (0) in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule: blue pixels move to the
    bottom row, replacing gray pixels.
    """
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Iterate through each column
    for j in range(cols):
        # Check for blue pixels in the column
        for i in range(rows):
            if input_grid[i][j] == 1:
                # Change the bottom-most gray pixel to blue in the output grid
                output_grid[rows - 1][j] = 1
                output_grid[i][j] = 0 # set cell in input grid that was a 1, now to zero.
                break  # Move to the next column after finding a blue pixel

    return output_grid