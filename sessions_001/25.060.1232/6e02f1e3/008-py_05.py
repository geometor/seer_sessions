"""
1.  **Identify the Main Diagonal:** Examine the input grid and identify the cells that form the main diagonal (top-left to bottom-right). A cell is on the main diagonal if its row index is equal to its column index.
2.  **Set Diagonal to Gray:** Change the color of all cells on the main diagonal to gray (5).
3.  **Set Off-Diagonal to White:** Change the value of all the cells *not* on the main diagonal to white (0).
4.  **Output:** The modified grid is the output. This process works for grids of any dimensions, including non-square grids. The main diagonal always exists.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid and apply the transformation.
    for i in range(rows):
        for j in range(cols):
            if i == j:  # Check for main diagonal
                output_grid[i, j] = 5  # set to gray (5)
            else:
                output_grid[i, j] = 0  # set to white (0)

    return output_grid