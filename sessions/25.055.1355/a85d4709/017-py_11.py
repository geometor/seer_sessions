"""
1. Preserve the shape of the input grid. The output grid will have the same dimensions.
2. If the center pixel of the input grid is gray (5), change it to yellow (4) in the output grid.
3. Change all white (0) pixels to red (2).
4. Change all the gray (5) pixels to red (2) if the center pixel of the input grid is *not* gray.
5. Change all gray(5) pixels to red(2), except the center pixel if it is gray (5).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    center_row = rows // 2
    center_col = cols // 2

    # Change all white (0) pixels to red (2)
    output_grid[output_grid == 0] = 2

    # check if center pixel is Gray
    if input_grid[center_row, center_col] == 5:
        output_grid[center_row, center_col] = 4

    # Change all gray pixels to red
    output_grid[output_grid == 5] = 2
    
    return output_grid