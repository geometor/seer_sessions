"""
1.  **Identify the 2x2 subgrid**: Locate the 2x2 subgrid at the bottom right corner of the input grid.
2.  **Check colors**: The colors present in the output bottom right are derived from colors on the input edges that are not white (0).
3. **Fill Subgrid**: Fill this 2x2 subgrid such that, replace any 0 (white) with the color to its right, top, top right.
4. The top left cell of the grid is untouched.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Fill the bottom right 2x2 subgrid
    for i in range(rows - 2, rows):
        for j in range(cols - 2, cols):
            if output_grid[i,j] == 0:
                if i == rows-2 and j == cols -2 :
                  if input_grid[i,j+1] != 0:
                     output_grid[i, j] = input_grid[i,j+1]
                elif i == rows-2 and j == cols -1:
                    output_grid[i,j] = input_grid[i,j]

                elif i == rows-1 and j == cols-2:
                    if input_grid[i-1,j+1] !=0:
                       output_grid[i,j] = input_grid[i-1,j+1]
                    elif input_grid[i,j+1] != 0:
                         output_grid[i,j] = input_grid[i,j+1]
                    elif input_grid[i-1,j] != 0:
                       output_grid[i, j] = input_grid[i-1,j]


                elif i == rows -1 and j == cols-1 :
                    if input_grid[i-1,j] != 0:
                        output_grid[i,j] = input_grid[i-1,j]

    return output_grid