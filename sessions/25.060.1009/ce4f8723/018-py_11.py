"""
1. **Extract Subsection:** Extract the top-left 4x4 subsection from the input grid.
2. **Recolor:** Within this 4x4 subsection, replace all non-zero color values with the value 3 (green). Leave the 0 (white) values unchanged.
3. **Output:** The resulting 4x4 grid is the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting the top-left 4x4 subsection
    and recoloring non-zero pixels to green (3).
    """
    # Initialize output grid as a 4x4 array filled with zeros.
    output_grid = np.zeros((4, 4), dtype=int)

    # Extract the 4x4 subsection and recolor.
    for i in range(4):
        for j in range(4):
            if input_grid[i][j] != 0:
                output_grid[i][j] = 3
            else:
                output_grid[i][j] = 0 # could skip, already initialized, but explicit
    return output_grid