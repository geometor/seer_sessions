"""
The transformation rule is as follows:
1. Identify two regions in the input grid: the top three rows (all white) and the bottom two rows (mixed colors).
2. The bottom two rows are preserved in the output grid.
3. In the top region (first three rows), change only the color of the leftmost and rightmost cells of the third row. The color of the pixels change from white (0) to blue (1).
4. The other pixels of input grid remain the same.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]

    # Check if there are at least 3 rows before proceeding
    if rows >= 3:
        # Change the color of the leftmost and rightmost pixels of the third row to blue (1)
        output_grid[2, 0] = 1
        output_grid[2, -1] = 1

    return output_grid