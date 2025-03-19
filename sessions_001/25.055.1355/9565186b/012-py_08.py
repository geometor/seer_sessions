"""
Based on the analysis of the failing examples, the initial transformation rule is incorrect. A revised rule is proposed:

1.  **Object Identification:** Identify contiguous blocks of pixels of the same color as distinct objects. The background is white (0).

2.  **Color Transformation Rules:**
    *   Blue (1), Gray (5), Black (0), and Azure(8) objects remain unchanged.
    *   Yellow (4) also remains unchanged.
    *   Red (2) objects are transformed to Yellow (4).
    *   Green (3) objects are transformed to Orange (7).

"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for i in range(rows):
        for j in range(cols):
            # Check the color and apply the transformation rule
            if input_grid[i, j] in [1, 5, 0, 4, 8]:  # Blue, Gray, Black, Yellow and Azure remain unchanged
                continue  # Do nothing
            elif input_grid[i, j] == 2:  # Red changes to Yellow
                output_grid[i, j] = 4
            elif input_grid[i, j] == 3:  # Green changes to Orange
                output_grid[i, j] = 7

    return output_grid