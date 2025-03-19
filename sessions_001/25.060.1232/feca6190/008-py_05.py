"""
Transforms a 1x5 input grid into a 10x10 output grid. Each color in the input
grid generates a diagonal line in the output grid. Diagonals start on a
baseline running from (9,0) to (5,4). The starting point and length of each
diagonal correspond to the index of the color in the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 10x10 output grid filled with zeros.
    output_grid = np.zeros((10, 10), dtype=int)
    input_width = len(input_grid[0])
   
    # Iterate through each color in the input (from left to right, index 0 to 4)
    for n in range(input_width):
        # Determine the starting point on the baseline: (9 - n, n).
        start_row = 9 - n
        start_col = n
        
        # Get the color from the input grid at the current index.
        color = input_grid[0][n]

        # Draw a diagonal line of pixels upwards and to the right.
        # Length of the diagonal is n + 1.
        for i in range(n + 1):
            row = start_row - i
            col = start_col + i
            
            # Check bounds to ensure we don't go outside the grid.
            if 0 <= row < 10 and 0 <= col < 10:
                output_grid[row][col] = color

    return output_grid