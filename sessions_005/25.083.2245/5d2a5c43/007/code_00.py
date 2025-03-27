"""
1.  **Determine Output Grid Width**: The output grid always has a fixed width of 4 columns and the same number of rows as the input grid.
2.  **Determine Output Grid Start**: The output grid always starts from the leftmost edge (column 0) of the input grid.
3.  **Create Subgrid**: Extract a subgrid from the input. The subgrid has the same height as the input grid. It starts from column 0 of the input grid and spans 4 columns to the right.
4.  **Replace Colors:** Within the extracted subgrid, replace all yellow (4) pixels with azure (8) pixels.
5.  **Output:** Return the modified subgrid.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Create subgrid (same height, width of 4, starting from column 0)
    output_grid = input_grid[:, 0:4].copy()

    # Replace yellow (4) with azure (8) within the subgrid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 4:
                output_grid[i, j] = 8

    return output_grid.tolist()