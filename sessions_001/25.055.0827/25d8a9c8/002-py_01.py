"""
Transforms a 3x3 input grid into a 3x3 output grid.
Top row becomes gray (5), all other rows become white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.  Avoids modifying original.
    output_grid = np.copy(input_grid)
    rows = len(output_grid)
    cols = len(output_grid[0]) if rows > 0 else 0 # Handle empty input case

    # Iterate through each row of the output grid.
    for i in range(rows):
        # If it is first row.
        if i == 0:
            # Change all pixels to gray
            for j in range(cols):
                output_grid[i][j] = 5
        # Other rows
        else:
            # Change all pixels to white.
            for j in range(cols):
                output_grid[i][j] = 0
    return output_grid