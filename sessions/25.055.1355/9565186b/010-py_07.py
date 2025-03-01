"""
1.  Identify Objects: The input consists of objects, which are contiguous blocks of pixels of the same color. Background is always white (0)
2.  Color Transformations:
    *   Blue (1) objects remain unchanged.
    *   Gray (5) objects remain unchanged.
    *   Black (0) objects remain unchanged.
    *   Yellow (4) remains unchanged.
    *   Green (3) and Red (2) objects are changed to Gray (5).
    *   Azure (8) is transformed to Gray (5)
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for i in range(rows):
        for j in range(cols):
            # Check the color and apply the transformation rule
            if input_grid[i, j] in [1, 5, 0, 4]:  # Blue, Gray, Black and Yellow remain unchanged
                continue # do nothing
            elif input_grid[i, j] in [3, 2, 8]:  # Green, Red and Azure change to Gray
                output_grid[i, j] = 5

    return output_grid