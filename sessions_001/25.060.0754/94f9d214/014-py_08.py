"""
The transformation identifies 2x2 squares of the same color in the input grid.
If a 2x2 square of the same color is found, the corresponding cell in the output grid is colored red (2).
All other cells (where a 2x2 square of the SAME color does not exist) in the output grid, remain at the default initialization, which is white/background (0).
The output grid is half the size of the input grid in each dimension (rows and columns).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with zeros, half the size of the input grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows // 2, cols // 2), dtype=int)

    # Iterate through the input grid, checking for 2x2 squares.
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Extract 2x2 subgrid
            subgrid = input_grid[i:i+2, j:j+2]

            # Check if all elements in the subgrid are the same
            if np.all(subgrid == subgrid[0, 0]):
                # Map the position to the output grid (integer division)
                output_row = i // 2
                output_col = j // 2

                # Set the corresponding output cell to red (2)
                output_grid[output_row, output_col] = 2

    return output_grid.tolist()