"""
The transformation involves changing the color of certain white pixels in the corners based on location, while preserving the existing gray-colored pixels. The input seems to have been divided in 9 regions. Six of the regions remain unchanged, while three of them change.
1.  **Identify static elements**: The gray (5) pixels in the input grid remain unchanged in the output grid. Specifically, two solid horizontal gray lines and gray lines in columns 3 and 8 remain.
2.  **Top Region**: The white (0) pixels in the top-left 3x3 subgrid of the input is colored blue(1).
3. **Middle Region:** The white(0) pixels of the 3 x 3 sub-grid at input[5:8, 4:8] are colored red(2).
4.  **Bottom Region**:The white (0) pixels in the bottom-right 3x3 subgrid of the input is colored green(3).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Top-left 3x3 subgrid: Change white (0) to blue (1).
    for i in range(3):
        for j in range(3):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 1

    #Middle-region: Change the white (0) pixels to red(2).
    for i in range(4,7):
        for j in range(3,7):
            if output_grid[i,j] == 0:
                output_grid[i,j] = 2
    # Bottom-right 3x3 subgrid: Change white (0) to green (3).
    for i in range(7, 10):
        for j in range(7, 10):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 3

    return output_grid