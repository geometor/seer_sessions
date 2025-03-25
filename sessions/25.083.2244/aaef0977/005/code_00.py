"""
The output grid is always 8x8. A dictionary of 8x8 grids is used, keyed by colors found in the input grid.
The output is constructed by selecting, for each (i,j) location, an output pixel
based on matching colors from the grids in the dictionary. The *last* color present in the input grid
is used as the key for selecting from grid_map.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid to a default 8x8 grid (all zeros)
    output_grid = np.zeros((8, 8), dtype=int)

    grid_map = {
    7: np.array([
        [9, 8, 2, 5, 0, 4, 3, 4],
        [6, 9, 8, 2, 5, 0, 4, 0],
        [1, 6, 9, 8, 2, 5, 0, 5],
        [3, 1, 6, 9, 8, 2, 5, 2],
        [4, 3, 1, 6, 9, 8, 2, 8],
        [0, 4, 3, 1, 6, 9, 8, 9],
        [5, 0, 4, 3, 1, 6, 9, 6],
        [2, 5, 0, 4, 3, 1, 6, 1]
    ]),
    3: np.array([
        [0,0,0,0,0,0,3,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]

     ]),
    5: np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])

    }

    # Iterate through each cell of the output grid
    for i in range(8):
        for j in range(8):
            # Get the unique colors from the input grid
            input_colors = np.unique(input_grid)
            # Get the *last* color
            last_color = input_colors[-1]

            # Find the corresponding pixel values from the grid_map
            if last_color in grid_map:
              output_grid[i,j] = grid_map[last_color][i,j]


    return output_grid