"""
1.  **Focus Area:** Consider only the top-left 4x4 section of the input grid.
2.  **Identify primary shape:** In the area of interest, identify locations of color 7 (orange).
3. **Replace color:** Create an output grid 4x4 where identified locations are color 3, every other cell is 0.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the top-left 4x4 subgrid of the input.
    for i in range(4):
        for j in range(4):
            # Check if the current cell in the input grid is orange (7).
            if input_grid[i][j] == 7:
                # Set the corresponding cell in the output grid to green (3)
                output_grid[i][j] = 3

    return output_grid