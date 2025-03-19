"""
1.  **Identify Objects:** Locate all colored squares (1x1 squares) in the input grid.
2.  **Group Objects by Proximity**: Notice how some squares of various colors form separated two by two square clusters.
3.  **Fill Grouped Squares with Green:** The program identifies where the original 2x2 squares were. If a 2 by 2 square of four distinct colored squares is identified, replace each identified square with a 2x2 area filled in with color green (value 3).
"""

import numpy as np

def find_2x2_squares(grid):
    """Finds 2x2 squares of non-zero colors."""
    squares = []
    for i in range(grid.shape[0] - 1):
        for j in range(grid.shape[1] - 1):
            if (grid[i, j] != 0 and grid[i+1, j] != 0 and
                grid[i, j+1] != 0 and grid[i+1, j+1] != 0):
                squares.append((i, j))
    return squares

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Find the 2x2 squares
    squares = find_2x2_squares(input_grid)

    # Fill identified 2x2 squares with green (3)
    for i, j in squares:
        output_grid[i:i+2, j:j+2] = 3

    return output_grid