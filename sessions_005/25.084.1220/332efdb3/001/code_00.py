"""
Creates a new grid of the same dimensions as the input grid.
Iterates through each cell (r, c) of the new grid.
If the row index r is even, the cell color is set to blue (1).
If the row index r is odd, the cell color alternates between blue (1) for even column indices c and white (0) for odd column indices c.
The input grid content is ignored, only its dimensions are used.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a checkerboard-like pattern based on row and column indices.
    Even rows are all blue (1).
    Odd rows alternate blue (1) and white (0), starting with blue.
    """
    # Get the dimensions of the input grid
    height = input_grid.shape[0]
    width = input_grid.shape[1]

    # Initialize the output grid with the same dimensions, filled with zeros initially
    # Using np.empty might be slightly more efficient if we are sure to fill every cell.
    output_grid = np.zeros((height, width), dtype=int)

    # Iterate through each cell of the grid by row and column index
    for r in range(height):
        for c in range(width):
            # Check if the row index is even
            if r % 2 == 0:
                # If the row index is even, set the cell to blue (1)
                output_grid[r, c] = 1
            else:
                # If the row index is odd, check the column index
                if c % 2 == 0:
                    # If the column index is even, set the cell to blue (1)
                    output_grid[r, c] = 1
                else:
                    # If the column index is odd, set the cell to white (0)
                    # This cell is already 0 due to initialization, but explicitly setting for clarity
                    output_grid[r, c] = 0

    # Return the completed output grid
    return output_grid
