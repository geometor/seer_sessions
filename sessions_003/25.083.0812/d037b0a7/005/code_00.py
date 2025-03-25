"""
1.  **Identify Seed Pixels:** Find non-zero pixels along the top edge (row 0) and the left edge (column 0) of the input grid. These are the "seed" pixels.

2.  **Column Propagation:** For each seed pixel in the top row, change the color of all *originally zero* pixels in its column to the color of the seed pixel.

3.  **Row Propagation:** For each seed pixel in the left column, change the color of all *originally zero* pixels in its row to the color of the seed pixel.

4. **Precedence/Interaction:** If both a row seed and a column seed want to change an originally zero cell, the expected result must be checked. Based on the available examples: it seems the output should take the color of the seed pixel in the first row or column of the *input grid*.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])
    original_grid = np.copy(input_grid) # create copy to check original zeros


    # Column Propagation
    for j in range(width):
        if input_grid[0][j] != 0:
            for i in range(height):
                if original_grid[i][j] == 0:  # Only propagate to originally zero cells
                    output_grid[i][j] = input_grid[0][j]

    # Row Propagation
    for i in range(height):
        if input_grid[i][0] != 0:
            for j in range(width):
                if original_grid[i][j] == 0: # Only propagate to originally zero cells
                    output_grid[i][j] = input_grid[i][0]

    return output_grid