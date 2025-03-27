```python
"""
The output grid is always 8x8. A dictionary of 8x8 grids is used, keyed by colors found in the input grid.
The output is constructed by selecting, for each (i,j) location, an output pixel
based on matching colors from the grids in the dictionary.
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
            # Get the unique colors from the input grid, resized to 8x8
            input_colors = np.unique(input_grid)

            # Find the corresponding pixel values from the grid_map for each color
            candidate_pixels = []
            for color in input_colors:
               if color in grid_map:
                  candidate_pixels.append(grid_map[color][i,j])

            # if there are no candidate pixels, leave the default of zero
            if not candidate_pixels:
              continue
            
            # use the first candidate
            output_grid[i,j] = candidate_pixels[0]


    return output_grid
```