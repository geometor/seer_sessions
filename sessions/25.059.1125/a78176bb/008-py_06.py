"""
1. Create Diagonals: Draw two diagonals on the grid.
2. Top-Left to Bottom-Right: One diagonal extends from the top-left corner to the bottom-right corner.
3. Top-Right to Bottom-Left: The other diagonal extends from the top-right corner to the bottom-left corner.
4. Color: Set the color of both diagonals to orange (7).
5. Removal: change any non-black pixel that is *not* on either diagonal to black.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Create top-left to bottom-right and top-right to bottom-left diagonals with orange color (7)
    for i in range(rows):
        for j in range(cols):
            # Top-left to bottom-right diagonal
            if i == j:
                output_grid[i, j] = 7
            # Top-right to bottom-left diagonal
            if i + j == rows - 1:
                output_grid[i, j] = 7

    # Iterate through the grid and set non-diagonal, non-black pixels to black (0)
    for i in range(rows):
      for j in range(cols):
        if (i !=j) and (i + j != rows - 1) and output_grid[i,j] != 0:
          output_grid[i,j] = 0

    return output_grid